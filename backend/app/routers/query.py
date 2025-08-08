from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    docId: str

class QueryResponse(BaseModel):
    answer: str
    source: str

@router.post("/query", response_model=QueryResponse)
async def handle_query(q: QueryRequest):
    return QueryResponse(answer=f"Echo: {q.question}", source=q.docId)
