from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

#from math_qa import answer_query, DEFAULT_NAMESPACE
from fastapi.middleware.cors import CORSMiddleware
from Gemini import answer_query, DEFAULT_NAMESPACE




app = FastAPI(
    title="Math Tutor API",
    description="An API for answering math questions using embedded textbook content.",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)




class QueryRequest(BaseModel):
    question: str
    namespace: Optional[str] = DEFAULT_NAMESPACE

class Citation(BaseModel):
    source: str
    page: int

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    disclaimer: str

@app.post("/answer", response_model=QueryResponse)
def get_answer(data: QueryRequest):
    try:
        result = answer_query(data.question, data.namespace)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
