from google import genai
from google.genai import types
from app.chunking.chunk import getAllChunks
from qdrant_client.models import PointStruct
from app.core.qdrant import client
from uuid import uuid4

client_g = genai.Client(
    vertexai=True,
    project="learncloud-501101",
    location="asia-south1",
)

def getEmbeddings(query:list[str]):
    response = client_g.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=1536,
        ),
    )

    return [embedding.values for embedding in response.embeddings]


def save_embeddings():
    
    all_chunks=getAllChunks()
    texts = [chunk.text for chunk in all_chunks]
    embeddings = getEmbeddings(texts)
    points = []

    for chunk, embedding in zip(all_chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "source": chunk.source,
                    "path": chunk.path,
                    "text": chunk.text,
                    "chunk_index": chunk.chunk_index,
                },
            )
        )

    operation_info = client.upsert(
        collection_name="documents",
        wait=True,
        points=points,
    )

    print(operation_info)