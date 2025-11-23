import streamlit as st
import requests
import json
import os

# Page Config
st.set_page_config(page_title="Autonomous QA Agent", layout="wide")
st.title("🤖 Autonomous QA Agent")

# Sidebar Configuration
st.sidebar.header("Configuration")
BACKEND_URL = st.sidebar.text_input("Backend URL", value="http://localhost:8000")

# State Management
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'generated_scripts' not in st.session_state:
    st.session_state.generated_scripts = {}
if 'html_content' not in st.session_state:
    st.session_state.html_content = ""

# Tabs
tab1, tab2, tab3 = st.tabs(["📂 Ingestion", "🧠 Planning", "📜 Scripting"])

# --- Tab 1: Ingestion ---
with tab1:
    st.header("Ingest Documentation & Assets")
    st.markdown("Upload your project documentation (Markdown, Text) and the target HTML file.")
    
    uploaded_files = st.file_uploader(
        "Upload HTML, Markdown, Text, JSON, or PDF files", 
        accept_multiple_files=True,
        type=['html', 'md', 'txt', 'json', 'pdf']
    )
    
    if st.button("Ingest Files"):
        if uploaded_files:
            files = []
            for f in uploaded_files:
                files.append(('files', (f.name, f.getvalue(), f.type)))
            
            try:
                with st.spinner("Ingesting files and building knowledge base..."):
                    response = requests.post(f"{BACKEND_URL}/ingest", files=files)
                    
                if response.status_code == 200:
                    st.success(f"Success! {response.json().get('message')}")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
        else:
            st.warning("Please upload at least one file.")

# --- Tab 2: Planning ---
with tab2:
    st.header("Test Planning")
    st.markdown("Describe the feature or flow you want to test. The agent will generate test cases based on the ingested documentation.")
    
    query = st.text_area("Describe what you want to test", value="Test the checkout flow including promo code validation.")
    
    if st.button("Generate Test Cases"):
        if query:
            try:
                with st.spinner("Analyzing documentation and generating test cases..."):
                    payload = {"query": query}
                    response = requests.post(f"{BACKEND_URL}/generate-tests", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.test_cases = data.get("test_cases", [])
                    if not st.session_state.test_cases:
                        st.warning("Generated 0 test cases. Please ensure you have **Ingested Files** in the first tab and that your API keys are correct.")
                    else:
                        st.success(f"Generated {len(st.session_state.test_cases)} test cases.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
        else:
            st.warning("Please enter a query.")

    # Display Test Cases
    if st.session_state.test_cases:
        st.subheader("Generated Test Cases")
        for tc in st.session_state.test_cases:
            with st.expander(f"{tc.get('id')} - {tc.get('description')}"):
                st.write(f"**Steps:**")
                for step in tc.get('steps', []):
                    st.write(f"- {step}")
                st.write(f"**Expected Result:** {tc.get('expected_result')}")
                if tc.get('grounded_in'):
                    st.info(f"📄 **Grounded In:** {tc.get('grounded_in')}")

# --- Tab 3: Scripting ---
with tab3:
    st.header("Selenium Script Generation")
    
    if not st.session_state.test_cases:
        st.info("Please generate test cases in the Planning tab first.")
    else:
        # Select Test Case
        tc_options = {f"{tc['id']} - {tc['description']}": tc for tc in st.session_state.test_cases}
        selected_option = st.selectbox("Select a Test Case", list(tc_options.keys()))
        selected_tc = tc_options[selected_option]
        
        st.subheader("Target Page Source")
        
        # Helper to load local asset
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Load 'checkout.html' Asset"):
                try:
                    paths_to_check = [
                        os.path.join("assets", "checkout.html"),
                        os.path.join("..", "assets", "checkout.html"),
                        os.path.join("qa_agent", "assets", "checkout.html"),
                        os.path.join("c:/Users/irish/OneDrive/Desktop/qa_agent/assets/checkout.html") # Absolute fallback
                    ]
                    
                    found = False
                    for path in paths_to_check:
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                st.session_state.html_content = f.read()
                                found = True
                                st.success(f"Loaded from {path}")
                                break
                    
                    if not found:
                        st.error("Could not find checkout.html locally. Please paste it manually.")
                        
                except Exception as e:
                    st.error(f"Error loading file: {e}")

        html_content = st.text_area(
            "Paste the raw HTML of the page to test (or load from assets)", 
            value=st.session_state.html_content, 
            height=200, 
            key="html_input"
        )
        # Update session state if user types manually
        st.session_state.html_content = html_content

        if st.button("Generate Script"):
            if html_content:
                try:
                    with st.spinner("Generating Selenium script..."):
                        payload = {
                            "test_case": selected_tc,
                            "html_content": html_content
                        }
                        response = requests.post(f"{BACKEND_URL}/generate-script", json=payload)
                    
                    if response.status_code == 200:
                        script_code = response.json().get("script_code")
                        st.session_state.generated_scripts[selected_tc['id']] = script_code
                        st.success("Script generated!")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
            else:
                st.warning("Please provide HTML content.")

        # Display Script
        if selected_tc['id'] in st.session_state.generated_scripts:
            st.subheader("Generated Python Script")
            script_code = st.session_state.generated_scripts[selected_tc['id']]
            st.code(script_code, language="python")
            
            st.markdown("### 🏃 How to Run")
            st.markdown("""
            1. **Copy** the code above.
            2. **Save** it to a file, e.g., `test_script.py`.
            3. **Install Selenium**: `pip install selenium`
            4. **Run**: `python test_script.py`
            
            > **Note**: Ensure the `driver.get(...)` URL in the script points to the correct location of your `checkout.html` file.
            """)
