from google.genai import types
from .embedding import getEmbeddings
from app.core.qdrant import client
from app.core.google import client_google
import json
from .prompt import SYSTEM_PROMPT
from app.core.session_storage import storage

def getVectorResult(query:str, limit:int=3):
    vectors=getEmbeddings(query)
    search_result = client.query_points(
        collection_name="documents",
        query=vectors[0],
        with_payload=True,
        limit=limit
    ).points
    return search_result

def generate_helper(data: dict, identifier: str = "") -> str:
    response = client_google.models.generate_content(
        model="gemini-2.5-flash",
        contents=json.dumps(data, indent=2, ensure_ascii=False),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.1,
            max_output_tokens=512,
        ),
    )

    answer = response.text

    if identifier:
        storage.add(identifier, data["query"], answer)

    return answer

def generate_answer(query:str, identifier:str="")->str:
    res = getVectorResult(query)

    data = {
        "query": query,
        "search_results": [
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload,
            }
            for point in res
        ],
    }

    if identifier:
        history=storage.get(identifier)
        if history:
            data["history"]=history
        else:
            print("Not found")

    return generate_helper(data, identifier)