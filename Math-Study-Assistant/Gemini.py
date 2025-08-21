import os, uuid, orjson
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from pypdf import PdfReader
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
import json

# -----------------------------
# Config
# -----------------------------
GEMINI_API_KEY   = ""
PINECONE_API_KEY = ""
PINECONE_INDEX   = ""

EMBED_MODEL = "models/embedding-001"
GEN_MODEL   = "gemini-1.5-flash"

TOP_K = 10            # fetch more chunks
MIN_SIM = 0.1         # lower threshold for better recall
CHUNK_TOKENS = 400
CHUNK_OVERLAP = 49
DEFAULT_NAMESPACE = "math_textbook"

MAX_CHUNK_TEXT = 2000  # chars per chunk before embedding
PREVIEW_LEN = 500      # chars stored in metadata

genai.configure(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

if PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=768,  # Gemini embeddings are 768-d
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

    # embed in batches
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
# Retrieval + QA
# -----------------------------
SYSTEM_PROMPT = (
    "You are a helpful **math tutor assistant**.\n"
    "Rules: Answer the question. you may use textbook as reference\n"
)
DISCLAIMER = "Educational use only. Always double-check solutions."

def retrieve(query: str, namespace: str = DEFAULT_NAMESPACE, k: int = TOP_K) -> List[Dict[str, Any]]:
    resp = genai.embed_content(
        model=EMBED_MODEL,
        content=query,
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=768
    )
    qvec = flatten_embedding(resp["embedding"])
    res = index.query(vector=qvec, top_k=k, include_metadata=True, namespace=namespace)
    hits = []
    for m in res.matches or []:
        if getattr(m, "score", 1.0) >= MIN_SIM:
            hits.append({**(m.metadata or {}), "_score": m.score, "_id": m.id})
    return hits

def build_messages(query: str, ctx: List[Dict[str, Any]]):
    ctx_str = "\n---\n".join([f"[{c['source']}, p.{c['page']}]\n{c['text'][:1000]}" for c in ctx])
    user = f"Q: {query}\n\nContext:\n{ctx_str}\n\nProvide a clear step-by-step solution. Add Disclaimer line."
    return [{"role": "user", "parts": [SYSTEM_PROMPT + "\n\n" + user]}]

def answer_query(query: str, namespace: str = DEFAULT_NAMESPACE):
    ctx = retrieve(query, namespace, TOP_K)
    msgs = build_messages(query, ctx)
    model = genai.GenerativeModel(GEN_MODEL)
    resp = model.generate_content(msgs)
    return {
        "answer": resp.text.strip(),
        "citations": [{"source": c["source"], "page": c["page"]} for c in ctx],
        "disclaimer": DISCLAIMER
    }

# -----------------------------
# Fine-tune dataset builder
# -----------------------------
def build_ft_example(question: str, ctx: List[Dict[str, Any]]):
    cites = ", ".join([f"{c['source']}, p.{c['page']}" for c in ctx[:3]])
    answer = f"Step-by-step solution: <your curated solution>\n\nCitations: [{cites}]\nDisclaimer: {DISCLAIMER}"
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
    }

def write_jsonl(records: List[Dict], path: str):
    with open(path, "wb") as f:
        for r in records:
            f.write(orjson.dumps(r))
            f.write(b"\n")


def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        query = body.get("query", "Explain Pythagorean theorem")
        namespace = body.get("namespace", DEFAULT_NAMESPACE)
    except json.JSONDecodeError:
        query = "Explain Pythagorean theorem"
        namespace = DEFAULT_NAMESPACE

    result = answer_query(query, namespace)
    return result
