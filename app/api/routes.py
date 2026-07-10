from fastapi import APIRouter
from pydantic import BaseModel
from .controller import getVectorResult, generate_helper

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
def generate_answer(query: UserInput):
    res = getVectorResult(query.query)

    data = {
        "query": query.query,
        "search_results": [
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload,
            }
            for point in res
        ],
    }

    return generate_helper(data)

# @router.get("/save")
# def saveEmbed():
#     save_embeddings()