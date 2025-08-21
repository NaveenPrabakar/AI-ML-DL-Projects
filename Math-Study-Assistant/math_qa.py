import os, uuid, orjson
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

from pypdf import PdfReader
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

try:
    import tiktoken
    ENCODER = tiktoken.get_encoding("cl100k_base")
except Exception:
    ENCODER = None


import os, uuid, orjson
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

from pypdf import PdfReader
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

try:
    import tiktoken
    ENCODER = tiktoken.get_encoding("cl100k_base")
except Exception:
    ENCODER = None

# ----------------------------- Config -----------------------------
OPENAI_API_KEY = ""
PINECONE_API_KEY = ""
PINECONE_INDEX  =  ""

EMBED_MODEL = "text-embedding-3-small"
GEN_MODEL   = "gpt-3.5-turbo"

TOP_K = 3
MIN_SIM = 0.3
DEFAULT_NAMESPACE = "math_textbook"

client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

if PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(PINECONE_INDEX)

# ----------------------------- Helper Functions -----------------------------
def num_tokens(s: str) -> int:
    if ENCODER:
        return len(ENCODER.encode(s))
    return max(1, len(s.split()) // 0.75)

@dataclass
class DocChunk:
    id: str
    text: str
    page: int
    meta: Dict[str, Any]

# ----------------------------- Retrieval + QA -----------------------------
SYSTEM_PROMPT = (
    "You are a helpful **math tutor assistant**.\n"
    "Rules: use ONLY provided textbook sources, explain step by step, and cite like [Source, p.Page].\n"
)
DISCLAIMER = "Educational use only. Always double-check solutions."



def retrieve(query: str, namespace: str = DEFAULT_NAMESPACE, k: int = TOP_K) -> List[Dict[str, Any]]:
    qvec = client.embeddings.create(model=EMBED_MODEL, input=[query]).data[0].embedding
    res = index.query(vector=qvec, top_k=k, include_metadata=True, namespace=namespace)
    hits = []
    for m in res.matches or []:
        if getattr(m,"score",1.0) >= MIN_SIM:
            hits.append({**(m.metadata or {}), "_score":m.score, "_id":m.id})
    return hits

def build_messages(query: str, ctx: List[Dict[str, Any]]):
    ctx_str = "\n---\n".join([f"[{c['source']}, p.{c['page']}]\n{c['text'][:1000]}" for c in ctx])
    user = f"Q: {query}\n\nContext:\n{ctx_str}\n\nProvide a clear step-by-step solution. Add Disclaimer line."
    return [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user}]

def answer_query(query: str, namespace: str = DEFAULT_NAMESPACE):
    ctx = retrieve(query, namespace, TOP_K)
    if not ctx:
        return {
            "answer": "Insufficient info in sources.",
            "citations": [],
            "disclaimer": DISCLAIMER
        }
    msgs = build_messages(query, ctx)
    resp = client.chat.completions.create(model=GEN_MODEL, messages=msgs, temperature=0.2)
    return {
        "answer": resp.choices[0].message.content.strip(),
        "citations": [{"source": c["source"], "page": c["page"]} for c in ctx],
        "disclaimer": DISCLAIMER
    }
