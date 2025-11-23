from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any

class IngestResponse(BaseModel):
    message: str
    files_processed: int

class TestCase(BaseModel):
    id: str
    description: str
    steps: List[str]
    expected_result: str
    grounded_in: str = Field(default="", description="Source document(s) this test is based on")
    
    model_config = ConfigDict(extra="ignore")

class TestGenerationRequest(BaseModel):
    query: str

class TestGenerationResponse(BaseModel):
    test_cases: List[TestCase]

class ScriptGenerationRequest(BaseModel):
    test_case: TestCase
    html_content: str = Field(..., description="Raw HTML content of the page to test")

class ScriptGenerationResponse(BaseModel):
    script_code: str
