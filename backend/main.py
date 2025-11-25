import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from typing import List, Optional
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

from models import (
    IngestResponse, 
    TestGenerationRequest, 
    TestGenerationResponse, 
    ScriptGenerationRequest, 
    ScriptGenerationResponse
)
from utils import parse_file_content
import database
import llm_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting QA Agent Backend...")
    yield
    print("Shutting down QA Agent Backend...")

app = FastAPI(title="Autonomous QA Agent API", lifespan=lifespan)

@app.post("/ingest", response_model=IngestResponse)
async def ingest_files(
    files: List[UploadFile] = File(...),
    x_gemini_api_key: Optional[str] = Header(None),
    x_qdrant_url: Optional[str] = Header(None),
    x_qdrant_api_key: Optional[str] = Header(None)
):
    """Ingests files (HTML, MD, TXT), creates embeddings, and stores them in Qdrant."""
    
    # Fallback to env vars if headers are missing
    gemini_key = x_gemini_api_key or os.environ.get("GEMINI_API_KEY")
    qdrant_url = x_qdrant_url or os.environ.get("QDRANT_URL")
    qdrant_key = x_qdrant_api_key or os.environ.get("QDRANT_API_KEY")

    if not gemini_key:
        raise HTTPException(status_code=400, detail="Gemini API Key is required (header or env var)")

    processed_count = 0
    documents = []
    embeddings = []

    for file in files:
        try:
            content = await file.read()
            text_content = parse_file_content(file.filename, content)
            
            embedding = llm_service.get_embedding(text_content, gemini_key)
            if not embedding:
                print(f"Skipping {file.filename}: Failed to generate embedding.")
                continue
                
            documents.append({
                "filename": file.filename,
                "content": text_content
            })
            embeddings.append(embedding)
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            continue

    if not documents:
        raise HTTPException(status_code=400, detail="No files were successfully processed.")

    try:
        database.upsert_documents(documents, embeddings, qdrant_url, qdrant_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return IngestResponse(message="Ingestion successful", files_processed=processed_count)

@app.post("/generate-tests", response_model=TestGenerationResponse)
async def generate_tests(
    request: TestGenerationRequest,
    x_gemini_api_key: Optional[str] = Header(None),
    x_qdrant_url: Optional[str] = Header(None),
    x_qdrant_api_key: Optional[str] = Header(None)
):
    """Generates test cases based on a user query using RAG."""
    
    gemini_key = x_gemini_api_key or os.environ.get("GEMINI_API_KEY")
    qdrant_url = x_qdrant_url or os.environ.get("QDRANT_URL")
    qdrant_key = x_qdrant_api_key or os.environ.get("QDRANT_API_KEY")

    if not gemini_key:
        raise HTTPException(status_code=400, detail="Gemini API Key is required")

    try:
        query_embedding = llm_service.get_embedding(request.query, gemini_key)
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to embed query.")

        context = database.search_documents(query_embedding, qdrant_url, qdrant_key, limit=3)
        test_cases = llm_service.generate_test_cases(context, gemini_key)
        
        return TestGenerationResponse(test_cases=test_cases)
        
    except Exception as e:
        print(f"ERROR in /generate-tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-script", response_model=ScriptGenerationResponse)
async def generate_script(
    request: ScriptGenerationRequest,
    x_gemini_api_key: Optional[str] = Header(None)
):
    """Generates a Selenium script for a specific test case."""
    
    gemini_key = x_gemini_api_key or os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        raise HTTPException(status_code=400, detail="Gemini API Key is required")

    try:
        script = llm_service.generate_selenium_script(request.test_case, request.html_content, gemini_key)
        return ScriptGenerationResponse(script_code=script)
    except Exception as e:
        print(f"ERROR in /generate-script: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
