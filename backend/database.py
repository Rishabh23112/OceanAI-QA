import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import uuid

qdrant_url = os.environ.get("QDRANT_URL")
qdrant_api_key = os.environ.get("QDRANT_API_KEY")

if not qdrant_url:
    print("Warning: QDRANT_URL not set. Using in-memory storage.")
    client = QdrantClient(":memory:")
else:
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

COLLECTION_NAME = "qa_agent_docs"

def ensure_collection():
    """Ensures the collection exists."""
    try:
        collections = client.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)
        
        if not exists:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
            )
    except Exception as e:
        print(f"Error ensuring collection: {e}")
        pass

def upsert_documents(documents: List[Dict[str, Any]], embeddings: List[List[float]]):
    """Upserts documents with their embeddings."""
    ensure_collection()
    
    points = []
    for doc, emb in zip(documents, embeddings):
        points.append(models.PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload=doc
        ))
    
    try:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"Successfully upserted {len(points)} documents.")
    except Exception as e:
        print(f"Error upserting documents: {e}")
        raise e

def search_documents(query_vector: List[float], limit: int = 5) -> str:
    """Searches for relevant documents and returns combined text."""
    ensure_collection()
    
    try:
        from qdrant_client.models import QueryRequest
        
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit
        ).points
        
    except Exception as e:
        print(f"Error during Qdrant search: {e}")
        raise e
    
    context = ""
    for res in results:
        context += f"\n--- Source: {res.payload.get('filename', 'Unknown')} ---\n"
        context += res.payload.get('content', '')
    
    return context
