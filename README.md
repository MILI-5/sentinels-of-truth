# 🛡️ Sentinels of Truth

### AI-Powered Multi-Agent Claim Verification System

Sentinels of Truth is an AI-powered claim verification system that investigates factual claims using a multi-agent workflow, evidence retrieval, structured reasoning, and a persistent knowledge base.

The user submits a claim, the backend processes it through the investigation graph, retrieves relevant evidence and knowledge-base matches, and produces a verification decision with confidence and reasoning.

---

## 🚀 Features

- **Claim Verification** — Analyze natural-language factual claims.
- **Multi-Agent Workflow** — Modular investigation pipeline built with LangGraph.
- **Evidence Retrieval** — Collect relevant supporting or contradicting evidence.
- **Knowledge Base** — Persistent ChromaDB-based storage for verified claims.
- **Confidence Scoring** — Provides a confidence value for the final decision.
- **Explainable Results** — Returns reasoning, evidence, search results, and knowledge-base matches.
- **REST API** — FastAPI backend for communication with the frontend.
- **Web Interface** — React + Vite frontend for submitting and viewing claims.

---

## 🏗️ Architecture

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
Investigation Graph
 │
 ├── Claim Analysis
 ├── Information Detection
 ├── Evidence / Search
 ├── Knowledge Base Retrieval
 └── Verification & Reasoning
 │
 ▼
Final Decision
 │
 ├── Confidence
 ├── Reasoning
 ├── Evidence
 └── Investigation Details
 ---

 ## 📁 Project Structure
sentinels-of-truth/
│
├── backend/
│   ├── agents/
│   │   ├── alpha.py
│   │   └── ...
│   ├── api.py
│   ├── database.py
│   ├── chroma_db.py
│   ├── graph.py
│   ├── models.py
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── data/
│   └── chroma/
│
├── requirements.txt
└── README.md

---
 ##🧠 Technology Stack

Frontend
React
Vite
JavaScript
CSS

Backend
Python
FastAPI
Uvicorn

AI / Agent Layer
LangGraph
LLM-based reasoning
Multi-agent workflow

Storage
ChromaDB
SQLite

Deployment
Vercel
Render

---

##🔌 API
Health Check
GET /

Returns the API status.

Health
GET /health

Database Health
GET /database-health

Investigate Claim
POST /investigate

Request:

{
  "claim": "The Earth revolves around the Sun."
}

The response contains the verification decision, confidence, reasoning, evidence, search results, knowledge-base matches, and investigation information.

---

##🗄️ Knowledge Base

The project uses ChromaDB as a persistent knowledge base.

The initial knowledge base contains verified claims such as:

The Earth revolves around the Sun.
Water freezes at 0°C under standard atmospheric pressure.
The Pacific Ocean is the largest ocean on Earth.

Additional claims can be added programmatically through the backend.

---

## ⚙️ Local Setup

1. Clone the repository
git clone https://github.com/MILI-5/sentinels-of-truth.git
cd sentinels-of-truth

2. Backend

Create and activate a virtual environment:

Windows

python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Start the backend:

uvicorn backend.api:app --reload

Backend:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
3. Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

---

## 🌐 Deployment

The application can be deployed as separate frontend and backend services.

Frontend: Vercel
Backend: Render

For production deployment, configure the frontend to use the deployed FastAPI backend URL and update the backend CORS configuration accordingly.

Example Render start command:

uvicorn backend.api:app --host 0.0.0.0 --port $PORT

🔍 Example

Input:

The Earth revolves around the Sun.

The system processes the claim through the investigation workflow and can return a result similar to:

Decision: VERIFIED
Confidence: 0.95

along with supporting reasoning and evidence.

🎯 Project Goal

The goal of Sentinels of Truth is to demonstrate how multi-agent AI, evidence retrieval, structured reasoning, and persistent knowledge bases can be combined to build an explainable claim verification system.

---


##📜 License

This project was developed as an academic/research project.

---

##🔮 Future Improvements

Potential future improvements include:

Additional specialized verification agents
More reliable web evidence retrieval
Source credibility scoring
Temporal reasoning for time-sensitive claims
Improved contradiction detection
Larger verified knowledge base
Citation-aware evidence generation
Claim history and tracking
User authentication
Investigation dashboards
Human-in-the-loop verification
Advanced vector search
Observability and agent tracing
Automated evaluation benchmarks
Better handling of ambiguous claims

---

##🧩 Design Principles

Sentinels of Truth is designed around the following principles:

Modularity

Each agent or processing stage has a focused responsibility.

Explainability

The system should provide evidence and reasoning rather than only returning a final label.

Extensibility

New agents, search providers, knowledge sources, and verification strategies can be added without redesigning the entire application.

Persistence

Verified knowledge can be stored and reused through the persistent knowledge base.

API-first Architecture

The frontend communicates with the backend through REST APIs, allowing the backend to be independently deployed and tested.