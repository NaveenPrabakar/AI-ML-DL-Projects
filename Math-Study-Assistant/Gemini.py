import os, uuid, orjson, json, redis
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from pypdf import PdfReader
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai

# -----------------------------
# Config
# -----------------------------
GEMINI_API_KEY   = ""
PINECONE_API_KEY = ""
REDIS_URL=""
PINECONE_INDEX   = ""

EMBED_MODEL = "models/embedding-001"
GEN_MODEL   = "gemini-1.5-flash"

TOP_K = 10
MIN_SIM = 0.1
CHUNK_TOKENS = 400
CHUNK_OVERLAP = 49
DEFAULT_NAMESPACE = "math_textbook"
MAX_CHUNK_TEXT = 2000
PREVIEW_LEN = 500
SESSION_TTL = 3600  # 1 hour session memory

genai.configure(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
rdb = redis.Redis.from_url(REDIS_URL, decode_responses=True)

if PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=768,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(PINECONE_INDEX)

# -----------------------------
# Helpers
# -----------------------------
@dataclass
class DocChunk:
    id: str
    text: str
    page: int
    meta: Dict[str, Any]

def num_tokens(s: str) -> int:
    return max(1, len(s.split()) // 0.75)

def pdf_to_pages(path: str) -> List[Tuple[int, str]]:
    reader = PdfReader(path)
    pages = []
    for i, p in enumerate(reader.pages, start=1):
        txt = p.extract_text() or ""
        txt = "\n".join(line.strip() for line in txt.splitlines())
        pages.append((i, txt))
    return pages

def chunk_text(text: str, page: int, tokens: int = CHUNK_TOKENS, overlap: int = CHUNK_OVERLAP):
    words, out, buf = text.split(), [], []
    for w in words:
        buf.append(w)
        if num_tokens(" ".join(buf)) >= tokens:
            out.append((" ".join(buf), page))
            buf = buf[-overlap:]
    if buf:
        out.append((" ".join(buf), page))
    return out

def safe_split_text(text, max_len=MAX_CHUNK_TEXT):
    pieces, start = [], 0
    while start < len(text):
        end = min(start + max_len, len(text))
        pieces.append(text[start:end])
        start = end
    return pieces

def flatten_embedding(embed):
    if isinstance(embed, list) and all(isinstance(x, (float,int)) for x in embed):
        return [float(x) for x in embed]
    elif isinstance(embed, list) and all(isinstance(x, list) for x in embed):
        return [float(x) for x in embed[0]]
    raise ValueError("Unexpected embedding shape")

# -----------------------------
# PDF → Pinecone ingestion
# -----------------------------
def ingest_pdf_safe(path: str, source: str, namespace: str = DEFAULT_NAMESPACE, year: int = 2024):
    pages = pdf_to_pages(path)
    chunks: List[DocChunk] = []

    for page, txt in pages:
        for chunk_txt, p in chunk_text(txt, page, tokens=CHUNK_TOKENS, overlap=CHUNK_OVERLAP):
            for piece in safe_split_text(chunk_txt, MAX_CHUNK_TEXT):
                cid = f"{source}-{p}-{uuid.uuid4().hex[:8]}"
                chunks.append(DocChunk(
                    id=cid,
                    text=piece,
                    page=p,
                    meta={"source": source, "page": p, "year": year, "namespace": namespace}
                ))

    upserts = []
    for i in range(0, len(chunks), 128):
        batch = chunks[i:i+128]
        texts = [c.text for c in batch]
        resp = genai.embed_content(model=EMBED_MODEL, content=texts)
        embeddings = []
        if isinstance(resp, dict) and "embedding" in resp:
            embeddings.append(flatten_embedding(resp["embedding"]))
        elif isinstance(resp, list):
            for r in resp:
                embeddings.append(flatten_embedding(r.get("embedding")))
        for c, vec in zip(batch, embeddings):
            if len(vec) != 768:
                raise ValueError(f"Embedding dimension mismatch: {len(vec)} != 768")
            upserts.append({
                "id": c.id,
                "values": vec,
                "metadata": {**c.meta, "text": c.text[:PREVIEW_LEN]}
            })

    for i in range(0, len(upserts), 100):
        index.upsert(vectors=upserts[i:i+100], namespace=namespace)

    return len(chunks)

# -----------------------------
# Retrieval + QA w/ session memory
# -----------------------------
SYSTEM_PROMPT = [
    "You are a helpful **math tutor assistant**.\n"
    "Rules: Answer the question. you may use textbook as reference\n"
    "Reject any irrelevant or harmful requests.\n",

    "You are a helpful **SQL assistant**.\n"
    "Rules: Use the provided context when applicable, provide correct and optimized SQL queries, and briefly explain your reasoning if needed.\n"
    "If relevant context is missing, inform the user instead of guessing.\n"
    "Reject any irrelevant or harmful requests.\n"
]
DISCLAIMER = "Educational use only. Always double-check solutions."
def retrieve(query: str, vector: str, namespace: str = DEFAULT_NAMESPACE, k: int = TOP_K) -> List[Dict[str, Any]]:
    resp = genai.embed_content(
        model=EMBED_MODEL,
        content=query,
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=768
    )
    grab = pc.Index(vector)
    qvec = flatten_embedding(resp["embedding"])
    res = grab.query(vector=qvec, top_k=k, include_metadata=True, namespace=namespace)
    hits = []
    for m in res.matches or []:
        if getattr(m, "score", 1.0) >= MIN_SIM:
            hits.append({**(m.metadata or {}), "_score": m.score, "_id": m.id})
    return hits

def build_messages(query: str, i:int, ctx: List[Dict[str, Any]], history: List[Dict[str,str]]):
    ctx_str = "\n---\n".join([f"[{c['source']}, p.{c['page']}]\n{c['text'][:1000]}" for c in ctx])
    user_content = f"Q: {query}\n\nContext:\n{ctx_str}\n\nProvide a clear step-by-step solution. Add Disclaimer line."

    msgs_text = SYSTEM_PROMPT[i] + "\n\n"
    # prepend previous session messages
    for h in history:
        role = h["role"]
        content = h["content"]
        msgs_text += f"{role.upper()}: {content}\n"

    msgs_text += f"USER: {user_content}"

    return [{"role": "user", "parts": [msgs_text]}]

def answer_query(query: str, vector: str, i: int, namespace: str = DEFAULT_NAMESPACE, session_id: str = None):
    session_id = session_id or str(uuid.uuid4())
    history = json.loads(rdb.get(session_id) or "[]")

    ctx = retrieve(query, vector, namespace, TOP_K)
    msgs = build_messages(query, i, ctx, history)
    model = genai.GenerativeModel(GEN_MODEL)
    resp = model.generate_content(msgs)

    answer = resp.text.strip()
    # update session memory
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": answer})
    rdb.set(session_id, json.dumps(history), ex=SESSION_TTL)

    return {
        "session_id": session_id,
        "answer": answer,
        "citations": [{"source": c["source"], "page": c["page"]} for c in ctx],
        "disclaimer": DISCLAIMER
    }

# -----------------------------
# Lambda handler
# -----------------------------
def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    choice = body.get("subject", "math")
    query = body.get("query", "Explain Pythagorean theorem")
    session_id = body.get("session_id")
    namespace = body.get("namespace", DEFAULT_NAMESPACE)

    if choice == "math":
        return answer_query(query, "math-index-gemini", 0, namespace, session_id)
    elif choice == "sql":
        return answer_query(query, "sql-index-gemini", 1, namespace, session_id)
