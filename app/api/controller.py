from google.genai import types
from .embedding import getEmbeddings
from app.core.qdrant import client
from app.core.google import client_google
import json
from .prompt import SYSTEM_PROMPT


def getVectorResult(query:str, limit:int=3):
    vectors=getEmbeddings(query)
    search_result = client.query_points(
        collection_name="documents",
        query=vectors[0],
        with_payload=True,
        limit=limit
    ).points
    return search_result

def generate_helper(data: dict) -> str:
    response = client_google.models.generate_content(
        model="gemini-2.5-flash",
        contents=json.dumps(data, indent=2, ensure_ascii=False),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.1,
            max_output_tokens=512,
        ),
    )

    return response.text

def generate_answer(query:str)->str:
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

    return generate_helper(data)