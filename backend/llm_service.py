import os
from google import genai
from google.genai import types
import json
from typing import List, Dict, Any
from .models import TestCase
from functools import lru_cache
from .utils import clean_html_for_llm
import re

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not set. LLM features will fail.")
client = genai.Client(api_key=api_key)

def get_embedding(text: str) -> List[float]:
    """Generates embedding for the given text."""
    try:
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        if response.embeddings and len(response.embeddings) > 0:
            return response.embeddings[0].values
        return []
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

@lru_cache(maxsize=10)
def generate_test_cases(context: str) -> List[Dict[str, Any]]:
    """Generates test cases based on the provided context."""
    prompt = f"""
    You are an expert QA Engineer. Based on the following documentation and UI guides, generate a list of comprehensive test cases.
    
    CRITICAL REQUIREMENT: Every test case MUST reference the source document(s) it is based on in the "grounded_in" field.
    Extract the document name from the context (e.g., "product_specs.md", "ui_guide.txt", "api_endpoints.json", "checkout.html").
    
    Context:
    {context}
    
    Output must be a JSON list of objects with the following structure:
    [
        {{
            "id": "TC001",
            "description": "Verify login with valid credentials",
            "steps": ["Enter username", "Enter password", "Click login"],
            "expected_result": "User is redirected to dashboard",
            "grounded_in": "product_specs.md"
        }}
    ]
    
    Each test case MUST include a "grounded_in" field indicating which document(s) the test requirements came from.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[TestCase]
            )
        )
        
        if response.text:
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                match = re.search(r'\[.*\]', text, re.DOTALL)
                if match:
                    try:
                        return json.loads(match.group(0))
                    except:
                        pass
                return []
            
        return []
    except Exception as e:
        print(f"Error generating test cases: {e}")
        return []

def generate_selenium_script(test_case: TestCase, html_content: str) -> str:
    """Generates a Selenium script for a specific test case."""
    cleaned_html = clean_html_for_llm(html_content)
    
    prompt = f"""
    You are an expert Automation Engineer. Write a robust Python Selenium script to execute the following test case.
    
    Test Case:
    ID: {test_case.id}
    Description: {test_case.description}
    Steps: {test_case.steps}
    Expected Result: {test_case.expected_result}
    
    Target HTML Page Source:
    {cleaned_html}
    
    Requirements:
    1. Use `selenium` version 4 with Microsoft Edge (pre-installed on Windows).
    2. Import these at the top (MINIMAL imports):
       - from selenium import webdriver
       - from selenium.webdriver.common.by import By
       - from selenium.webdriver.support.ui import WebDriverWait
       - from selenium.webdriver.support import expected_conditions as EC
    3. Initialize Edge simply like this (Selenium 4 auto-manages the driver):
       driver = webdriver.Edge()
    4. Use `WebDriverWait` and `expected_conditions` (EC) for all element interactions. DO NOT use `time.sleep()`.
    5. Assume the HTML file is local. Use `driver.get("file:///C:/Users/irish/OneDrive/Desktop/qa_agent/assets/checkout.html")` as the URL.
    6. Include assertions to verify the Expected Result.
    7. Wrap everything in a try-except-finally block with proper error handling.
    8. Return ONLY the Python code, no markdown formatting, no comments about webdriver-manager.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        text = response.text
        if text.startswith("```python"):
            text = text[9:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()
    except Exception as e:
        print(f"Error generating script: {e}")
        return f"# Error generating script: {str(e)}"
