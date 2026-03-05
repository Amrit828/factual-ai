# AI Misinformation Detection System

An end-to-end AI system that analyzes articles, extracts verifiable factual claims, retrieves evidence from a FAISS-indexed knowledge base, and determines if claims are **Supported**, **Refuted**, or **Unverifiable**.

## 🏗️ Technical Architecture

### Backend Stack
* **Framework:** FastAPI
* **Package Manager:** uv
* **LLM Runtime:** Ollama (running `qwen2.5:7b`)
* **Embeddings:** `bge-small-en` (via `sentence-transformers`)
* **Vector Database:** FAISS (Facebook AI Similarity Search)

### Frontend Stack
* **Framework:** React.js (Vite)
* **Styling:** Tailwind CSS v4
* **Features:** Real-time results panel with verdict badges, claim extraction, and evidence viewing.

---

## 🚀 The Verification Pipeline
1. **Input:** User submits raw article or text via the React frontend.
2. **Segmentation:** The backend splits the article into individual sentences.
3. **Claim Filtering:** The `qwen2.5:7b` LLM filters sentences to keep only verifiable factual claims.
4. **Embedding & Retrieval:** Claims are embedded using `bge-small-en` and matched against the FAISS index to find top-k evidence chunks.
5. **Reasoning:** The LLM compares the claim against the retrieved facts to determine the verdict.
6. **Structured Verdict:** Returns a JSON object containing the verdict (Supported, Refuted, Unverifiable), reasoning, and a confidence score.

---

## 🛠️ Setup Instructions

### Prerequisites
1. Install [uv](https://github.com/astral-sh/uv), the fast Python package installer.
2. Install [Node.js](https://nodejs.org/en) and `npm`.
3. Install [Ollama](https://ollama.com/) locally and pull the Qwen 2.5 7B model:
   ```bash
   ollama run qwen2.5:7b
   ```

### 1. Backend Setup

```bash
cd backend

# Create a virtual environment and install dependencies using uv
uv sync # Or uv pip install -r requirements.txt if exported

# Run the FastAPI server
uv run uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

### 3. Usage
- Open your browser to the Vite frontend URL (typically `http://localhost:5173` or `http://localhost:5174`).
- Paste an article containing claims into the text area.
- Click "Verify Article" to view the segmentation, extracted claims, and real-time verdicts.

---

## 📁 Project Structure

```text
misinformation-detector/
├── backend/
│   ├── check_models.py        # Utility script to check local models
│   ├── main.py                # FastAPI entry point
│   ├── api/routes.py          # POST /verify_article & /verify_claim
│   ├── pipeline/              # Extraction and verification logic
│   ├── retrieval/             # FAISS and retriever logic
│   ├── llm/                   # Ollama client integration
│   └── storage/               # Persistent index.faiss & metadata
└── frontend/                  # React application (Vite + Tailwind)
```
