import os, uuid, json, redis
from typing import List, Dict, Any
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import numpy as np
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

# -----------------------------
# Config
# -----------------------------
OPENAI_API_KEY   = ""
PINECONE_API_KEY = ""
REDIS_URL        = ""
INDEX_NAME       = "math"

DEFAULT_NAMESPACE = "math"
EMBED_MODEL       = "text-embedding-3-small"
GEN_MODEL         = "gpt-5-nano"
TOP_K             = 5
MIN_SIM           = 0.1
SESSION_TTL       = 3600  # 1 hour session memory
PREVIEW_LEN       = 500

# -----------------------------
# Clients
# -----------------------------
client = OpenAI(api_key=OPENAI_API_KEY)
rdb = redis.Redis.from_url(REDIS_URL, decode_responses=True)

pc = Pinecone(api_key=PINECONE_API_KEY)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(INDEX_NAME)

# -----------------------------
# Helpers
# -----------------------------
def extract_pages(pdf_path: str):
    """Extract text from PDF pages with OCR fallback."""
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text").strip()
        if not text:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img).strip()
        pages.append({"page_number": i+1, "text": text})
    return pages

def get_embedding(text: str) -> np.ndarray:
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    return np.array(resp.data[0].embedding, dtype='float32')

def ingest_pdf(pdf_path: str, source: str, namespace: str = DEFAULT_NAMESPACE):
    pages = extract_pages(pdf_path)
    upserts = []
    for p in pages:
        emb = get_embedding(p["text"])
        vec_id = f"{source}-{p['page_number']}-{uuid.uuid4().hex[:8]}"
        upserts.append({
            "id": vec_id,
            "values": emb.tolist(),
            "metadata": {
                "source": source,
                "page": p["page_number"],
                "text": p["text"][:PREVIEW_LEN]
            }
        })
    for i in range(0, len(upserts), 100):
        index.upsert(vectors=upserts[i:i+100], namespace=namespace)
    print(f"Ingested {len(pages)} pages from {source} into Pinecone.")

# -----------------------------
# System prompts
# -----------------------------
SYSTEM_PROMPTS = [
    "You are a helpful **math tutor assistant**.\n"
    "Rules: Use the Chat Histroy, Answer math questions clearly and accurately. Use step-by-step reasoning and textbook context when available.",

    "You are a helpful **SQL assistant**.\n"
    "Rules: Use the Chat Histroy, Write correct, efficient SQL queries using provided context if possible. Explain your queries briefly.",

    "You are a helpful **astronomy tutor assistant**.\n"
    "Rules: Use the chat histroy, Use textbook context when available and cite pages as [Source, p.Page]. Explain concepts clearly."
]

DISCLAIMER = "Educational use only. Always double-check solutions."

# -----------------------------
# Retrieval
# -----------------------------
def query_pinecone(query: str, top_k: int = TOP_K, namespace: str = DEFAULT_NAMESPACE):
    qvec = get_embedding(query)
    res = index.query(vector=qvec, top_k=top_k, include_metadata=True, namespace=namespace)
    hits = []
    for m in res.matches or []:
        if getattr(m, "score", 1.0) >= MIN_SIM:
            hits.append({
                "id": m.id,
                "score": m.score,
                "text": m.metadata.get("text", ""),
                "source": m.metadata.get("source", ""),
                "page": m.metadata.get("page", "")
            })
    return hits

def build_prompt(query: str, ctx: List[Dict[str, Any]], role_index: int, history: List[Dict[str, str]]):
    ctx_str = "\n---\n".join([f"[{c['source']}, p.{c['page']}]\n{c['text'][:1000]}" for c in ctx]) if ctx else ""
    if ctx:
        user_content = f"Q: {query}\n\nContext:\n{ctx_str}\nAnswer step by step.\nAdd a final line: '{DISCLAIMER}'"
    else:
        user_content = f"Q: {query}\n\nNo context found. Answer using general knowledge.\nAdd a final line: '{DISCLAIMER}'"

    # Combine system prompt, history, and user query
    msgs_text = SYSTEM_PROMPTS[role_index] + "\n\n"
    for h in history:
        msgs_text += f"{h['role'].upper()}: {h['content']}\n"
    msgs_text += f"USER: {user_content}"

    return [{"role": "user", "content": msgs_text}]

# -----------------------------
# Answer query with session memory
# -----------------------------
def answer_query(query: str, role_index: int, namespace: str = DEFAULT_NAMESPACE, session_id: str = None):
    session_id = session_id or str(uuid.uuid4())
    history = json.loads(rdb.get(session_id) or "[]")

    ctx = query_pinecone(query, TOP_K, namespace)
    prompt = build_prompt(query, ctx, role_index, history)
    resp = client.chat.completions.create(
        model=GEN_MODEL,
        messages=prompt
    )
    answer = resp.choices[0].message.content.strip()

    # Update session memory
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
# Lambda-style handler
# -----------------------------
def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    subject = body.get("subject", "math")
    query = body.get("query", "Explain Pythagorean theorem")
    session_id = body.get("session_id")
    namespace = body.get("namespace", DEFAULT_NAMESPACE)

    if subject == "math":
        return answer_query(query, 0, "math", session_id)
    elif subject == "sql":
        return answer_query(query, 1, "sql", session_id)
    elif subject == "astro":
        return answer_query(query, 2, "astro", session_id)
