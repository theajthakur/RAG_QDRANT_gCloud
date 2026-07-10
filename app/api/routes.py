from fastapi import APIRouter
from pydantic import BaseModel
from .controller import getVectorResult, generate_answer

router= APIRouter()

@router.get("/")
def greet():
    return {"message":"Hello"}

class UserInput(BaseModel):
    query: str

@router.post("/query")
def fetchQuery(req: UserInput):
    search_result=getVectorResult(req.query)
    return {
        "query": req.query,
        "search_results": search_result
    }

@router.post("/generate")
def generate_answer_route(query: UserInput):
    return generate_answer(query.query)

# @router.get("/save")
# def saveEmbed():
#     save_embeddings()