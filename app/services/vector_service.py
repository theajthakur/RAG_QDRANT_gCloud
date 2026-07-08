from qdrant_client.models import Distance, VectorParams
from app.core.qdrant import client
from app.core.config import settings


def create_collection():
    collections = client.get_collections()

    names = [c.name for c in collections.collections]

    if settings.QDRANT_COLLECTION not in names:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )