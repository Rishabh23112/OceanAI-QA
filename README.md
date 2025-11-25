# Autonomous QA Agent

An intelligent, autonomous QA agent capable of constructing a "testing brain" from project documentation. It generates comprehensive test cases and executable Selenium scripts grounded in your provided documents.

## Features
- **Knowledge Base Ingestion**: Uploads and processes HTML, Markdown, Text, JSON, and PDF files into a vector database (Qdrant).
- **Test Case Generation**: Uses Gemini LLM + RAG to generate test cases based on your documentation.
- **Selenium Script Generation**: Converts test cases into robust Python Selenium scripts.
- **Streamlit UI**: A user-friendly interface for the entire workflow.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Google Gemini API Key
- (Optional) Qdrant Cloud URL/Key (defaults to in-memory for local use)

### Installation
1.  Clone the repository.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

> [!NOTE]
> **No `.env` file required!** All API keys (Gemini API Key, Qdrant URL, and Qdrant API Key) are entered directly in the Streamlit frontend UI when you start the application.

## Usage

### 1. Run Locally (Two Terminals)
Start services individually if you prefer separate processes during development:

```bash
# Terminal 1
uvicorn backend.main:app --reload

# Terminal 2
streamlit run frontend/app.py
```

### 2. Docker (Single Container)

A single container now runs both FastAPI and Streamlit.

```bash
docker-compose up --build
```

- Streamlit UI: `http://localhost:8501`
- FastAPI docs (reachable from the container and via forwarded port if needed): `http://localhost:8000/docs`

> The container uses `start.sh` to launch FastAPI on port `8000` and Streamlit on the externally exposed port (`8501` by default). Streamlit talks to the API via `http://127.0.0.1:8000`.

### 3. Deploy on Render Using Docker

1. Push the repository to GitHub (already done if following prior instructions).
2. In Render, create a **Web Service** and choose **Docker** as the deployment method.
3. Point Render to this repository. The root `Dockerfile` installs dependencies, copies the code, and runs `start.sh`.
4. Set the following environment variables in Render (if needed):
   - `PORT`: Render sets this automatically; no change required.
   - `BACKEND_PORT`: default `8000`.
   - Any API keys (`GEMINI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`) if you prefer not to enter them via the Streamlit UI.
5. Deploy. Render exposes the Streamlit UI at the service URL, and the UI communicates with the FastAPI process running inside the same container.

### 4. Workflow
1.  **Configure API Keys**: When you open the Streamlit UI, enter your **Gemini API Key**, **Qdrant URL** , and **Qdrant API Key** in the sidebar. These are required for the application to function.
2.  **Ingest**: Go to the "Ingestion" tab. Upload your support documents (e.g., `assets/product_specs.md`) and the target HTML (`assets/checkout.html`). Click "Ingest Files".
3.  **Plan**: Go to the "Planning" tab. Describe what you want to test (e.g., "Test discount codes"). Click "Generate Test Cases".
4.  **Script**: Go to the "Scripting" tab. Select a generated test case. Ensure the target HTML is loaded. Click "Generate Script".
5.  **Run**: Copy the generated Python script and run it locally (can copy paste that code in test_run.py file and run it)to verify the test.

## Project Structure
- `backend/`: FastAPI application, LLM service, and Database logic.
- `frontend/`: Streamlit user interface.
- `start.sh`: Launch script that runs both FastAPI and Streamlit inside one container.
- `assets/`: Sample project files (`checkout.html`, `product_specs.md`, etc.).

## Support Documents
- `product_specs.md`: Defines pricing, promo codes, and validation rules.
- `ui_ux_guide.txt`: Defines visual and interaction requirements.
- `api_endpoints.json`: Mock API documentation for the checkout process.
