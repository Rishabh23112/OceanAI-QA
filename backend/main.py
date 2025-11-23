import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

from .models import (
    IngestResponse, 
    TestGenerationRequest, 
    TestGenerationResponse, 
    ScriptGenerationRequest, 
    ScriptGenerationResponse
)
from .utils import parse_file_content
from . import database
from . import llm_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting QA Agent Backend...")
    try:
        database.ensure_collection()
    except Exception as e:
        print(f"Startup Warning: Could not ensure collection: {e}")
    yield
    print("Shutting down QA Agent Backend...")

app = FastAPI(title="Autonomous QA Agent API", lifespan=lifespan)

@app.post("/ingest", response_model=IngestResponse)
async def ingest_files(files: List[UploadFile] = File(...)):
    """Ingests files (HTML, MD, TXT), creates embeddings, and stores them in Qdrant."""
    processed_count = 0
    documents = []
    embeddings = []

    for file in files:
        try:
            content = await file.read()
            text_content = parse_file_content(file.filename, content)
            
            embedding = llm_service.get_embedding(text_content)
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
        database.upsert_documents(documents, embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return IngestResponse(message="Ingestion successful", files_processed=processed_count)

@app.post("/generate-tests", response_model=TestGenerationResponse)
async def generate_tests(request: TestGenerationRequest):
    """Generates test cases based on a user query using RAG."""
    try:
        query_embedding = llm_service.get_embedding(request.query)
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to embed query.")

        context = database.search_documents(query_embedding, limit=3)
        test_cases = llm_service.generate_test_cases(context)
        
        return TestGenerationResponse(test_cases=test_cases)
        
    except Exception as e:
        print(f"ERROR in /generate-tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-script", response_model=ScriptGenerationResponse)
async def generate_script(request: ScriptGenerationRequest):
    """Generates a Selenium script for a specific test case."""
    try:
        script = llm_service.generate_selenium_script(request.test_case, request.html_content)
        return ScriptGenerationResponse(script_code=script)
    except Exception as e:
        print(f"ERROR in /generate-script: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
