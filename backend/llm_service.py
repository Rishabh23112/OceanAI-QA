import os
from google import genai
from google.genai import types
import json
from typing import List, Dict, Any, Optional
from models import TestCase
from functools import lru_cache
from utils import clean_html_for_llm
import re

def get_client(api_key: str):
    if not api_key:
        raise ValueError("Gemini API Key is required")
    return genai.Client(api_key=api_key)

def get_embedding(text: str, api_key: str) -> List[float]:
    """Generates embedding for the given text."""
    try:
        client = get_client(api_key)
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

def generate_test_cases(context: str, api_key: str) -> List[Dict[str, Any]]:
    """Generates test cases based on the provided context."""
    client = get_client(api_key)
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

def generate_selenium_script(test_case: TestCase, html_content: str, api_key: str) -> str:
    """Generates a Selenium script for a specific test case."""
    client = get_client(api_key)
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
       - import sys
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
    9. CRITICAL: For selectors, PREFER `data-*` attributes (e.g., `data-name`, `data-id`) over text content.
    10. If matching by text is necessary, use `normalize-space()` in XPath or `contains()` to handle potential whitespace issues. DO NOT use strict text equality for buttons.
    
    11. CRITICAL - CONSOLE OUTPUT REQUIREMENTS:
        - At the START of the try block, print a test header with the test case ID and description using "=" borders (70 chars wide)
        - Print "✓" before EACH major action with a descriptive message (e.g., "✓ Initializing Edge WebDriver...", "✓ Navigating to...", "✓ Locating element...", "✓ Clicking button...")
        - After successful test completion, print a SUCCESS message: "✅ TEST PASSED: [brief success description]" with "=" borders
        - In the except block, print a FAILURE message: "❌ TEST FAILED: [test name]" with error details and "=" borders, then call sys.exit(1)
        - In the finally block, print "✓ Closing browser..." before driver.quit() and "✓ Test execution complete." after
        - Make ALL output clear, informative, and easy to read
        - AFTER the test execution (at the end of try block, after SUCCESS message), ALWAYS print the structured test case summary with these fields on separate lines:
          * Test_ID: {test_case.id}
          * Feature: [extracted from test case description]
          * Test_Scenario: [extracted from test steps or description]
          * Expected_Result: {test_case.expected_result}
          * Grounded_In: {test_case.grounded_in}
        - Print a blank line before the summary for clarity
        - This summary should appear in BOTH success and failure scenarios
    
    Example template structure:
    ```python
    import sys
    from selenium import webdriver
    # ... other imports
    
    try:
        print("=" * 70)
        print("🧪 TEST CASE: [Test ID] - [Description]")
        print("=" * 70)
        
        print("\\n✓ Initializing Edge WebDriver...")
        driver = webdriver.Edge()
        
        print("✓ Navigating to HTML file...")
        driver.get("...")
        
        # ... more steps with print statements
        
        print("\\n" + "=" * 70)
        print("✅ TEST PASSED: [Success message]")
        print("=" * 70)
        
        # Print structured test case summary
        print()
        print("Test_ID: [TC-ID]")
        print("Feature: [Feature Name]")
        print("Test_Scenario: [Scenario Description]")
        print("Expected_Result: [Expected Result]")
        print("Grounded_In: [Document Name]")
        
    except Exception as e:
        print("\\n" + "=" * 70)
        print("❌ TEST FAILED: [Test name]")
        print("=" * 70)
        print(f"Error: {{str(e)}}")
        print("=" * 70)
        
        # Print structured test case summary on failure too
        print()
        print("Test_ID: [TC-ID]")
        print("Feature: [Feature Name]")
        print("Test_Scenario: [Scenario Description]")
        print("Expected_Result: [Expected Result]")
        print("Grounded_In: [Document Name]")
        
        sys.exit(1)
        
    finally:
        if 'driver' in locals() and driver:
            print("\\n✓ Closing browser...")
            driver.quit()
            print("✓ Test execution complete.\\n")
    ```
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
