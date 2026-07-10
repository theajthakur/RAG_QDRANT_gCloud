from fastapi import APIRouter
from pydantic import BaseModel
from .embedding import getEmbeddings, save_embeddings
router= APIRouter()

@router.get("/")
def greet():
    return {"message":"Hello"}

class UserInput(BaseModel):
    query: str

@router.post("/query")
def fetchQuery(req: UserInput):
    vectors=getEmbeddings(req.query)
    return {
        "query": req.query,
        "embeddings":vectors
    }

# @router.get("/save")
# def saveEmbed():
#     save_embeddings()