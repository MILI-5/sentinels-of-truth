**# 🛡️ Sentinels of Truth**

**### AI-Powered Multi-Agent Claim Verification & Knowledge Base System**

Sentinels of Truth is an AI-powered claim verification system designed to investigate factual claims using a multi-agent workflow, web evidence, structured reasoning, and a persistent knowledge base.

The system accepts a natural-language claim, investigates it through multiple processing stages, retrieves supporting or contradicting evidence, checks existing knowledge, and produces a final verification decision with confidence and reasoning.

**---**

**## 🚀 Overview**

Misinformation spreads quickly across the internet, making it difficult to determine whether a claim is reliable.

**\*\*Sentinels of Truth\*\*** addresses this problem by combining:

\- 🤖 Multi-agent AI workflow

\- 🔎 Evidence retrieval

\- 🧠 LLM-based reasoning

\- 🗄️ Persistent knowledge storage

\- 📚 ChromaDB vector database

\- ⚡ FastAPI backend

\- ⚛️ React frontend

\- 📊 Confidence-based verification

\- 🔗 Evidence and search-result tracking

**### Basic workflow**

\`\`\`text

User Claim

    ↓

React Frontend

    ↓

FastAPI Backend

    ↓

Investigation Graph

    ↓

┌───────────────────────────────┐

│       Multi-Agent Workflow    │

│                               │

│  Claim Analysis               │

│        ↓                      │

│  Information Detection        │

│        ↓                      │

│  Evidence / Search            │

│        ↓                      │

│  Knowledge Base Retrieval     │

│        ↓                      │

│  Verification & Reasoning     │

└───────────────────────────────┘

    ↓

Final Decision

    ↓

Confidence + Reasoning + Evidence

    ↓

React Frontend

✨ Features

1\. Claim Verification

Users can enter a factual claim such as:

The Earth revolves around the Sun.

The system investigates the claim and returns a verification result.

Possible outcomes include:

VERIFIED

FALSE

UNCERTAIN

2\. Multi-Agent Architecture

The backend uses a graph-based investigation workflow.

Each stage of the workflow is responsible for a specific part of the investigation process.

The architecture is designed to make the verification process modular and extensible.

3\. Knowledge Base

Sentinels of Truth maintains a persistent knowledge base using ChromaDB.

The initial knowledge base contains verified claims such as:

The Earth revolves around the Sun.



Water freezes at 0 degrees Celsius under standard atmospheric pressure.



The Pacific Ocean is the largest ocean on Earth.

The knowledge base can also be extended with additional claims.

4\. Evidence Retrieval

The system collects evidence relevant to the submitted claim.

Evidence and search results are maintained as part of the investigation state so that the final decision can be explained.

5\. Confidence Score

The system produces a confidence value associated with the final verification decision.

Example:

Decision: VERIFIED

Confidence: 0.94

6\. Explainable Results

Instead of returning only a binary result, the system provides:

Final decision

Confidence

Reasoning

Evidence

Search results

Search queries

Knowledge base matches

Contradiction information

Investigation history

Errors, if any

Project Architecture

sentinels-of-truth/

│

├── backend/

│   ├── agents/

│   │   ├── alpha.py

│   │   └── ...

│   │

│   ├── api.py

│   ├── database.py

│   ├── chroma\_db.py

│   ├── graph.py

│   ├── models.py

│   └── ...

│

├── frontend/

│   ├── src/

│   │   ├── App.jsx

│   │   ├── App.css

│   │   └── ...

│   │

│   ├── package.json

│   └── ...

│

├── data/

│   └── chroma/

│

├── requirements.txt

├── README.md

└── ...

The exact structure may evolve as additional agents, tools, and components are added

🧠 Backend

The backend is implemented in Python using FastAPI.

Main components

Component   Purpose

api.py  FastAPI application and API endpoints

graph.py    Investigation workflow / graph

models.py   Request and response models

database.py SQLite database functionality

chroma\_db.py    ChromaDB knowledge base

agents/ Individual investigation agents

API

The backend exposes a REST API.

Health Check

GET /

Returns:

{

  "message": "Sentinels of Truth API is running."

}

Health Endpoint

GET /health

Returns:

{

  "status": "healthy"

}

Database Health

GET /database-health

Used to verify the state of the application database.

Investigate Claim

POST /investigate

Request

{

  "claim": "The Earth revolves around the Sun."

}

Response

The response contains information such as:

{

  "claim\_id": "api\_xxxxxxxxxxxx",

  "claim": "The Earth revolves around the Sun.",

  "decision": "VERIFIED",

  "confidence": 0.95,

  "reasoning": "...",

  "evidence": [],

  "search\_results": [],

  "search\_queries": [],

  "verification\_report": {},

  "database\_matches": [],

  "contradiction\_info": {},

  "investigation\_history": [],

  "errors": []

}

The exact response depends on the investigation performed by the system.

🗄️ Knowledge Base

The project uses ChromaDB as a persistent vector database.

The knowledge base is initialized through:

initialize\_knowledge\_base()

The system prevents duplicate default claims from being inserted.

Claims can also be added programmatically using:

add\_claim(

    claim\_id="example\_001",

    text="Example verified claim",

    metadata={

        "source": "Example source",

        "type": "verified\_claim",

        "verification\_status": "verified"

    }

)

🎨 Frontend

The frontend is built using:

React

Vite

CSS

The frontend provides a simple interface where users can:

Enter a claim.

Submit the claim for investigation.

Wait for the AI investigation.

View the verification result.

View confidence and reasoning.

Inspect evidence and other investigation information.

Local Setup

1\. Clone the repository

git clone <[https://github.com/MILI-5/sentinels-of-truth](https://github.com/MILI-5/sentinels-of-truth)>

cd sentinels-of-truth

Backend Setup

Create a virtual environment:

Windows

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1

If PowerShell blocks activation, use:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate again:

.\venv\Scripts\Activate.ps1

Install Python dependencies

pip install -r requirements.txt

Run the Backend

From the project root:

uvicorn backend.api\:app --reload

The backend should be available at:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

FastAPI documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Run the Frontend

Open another terminal:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend should be available at:

[http://localhost:5173](http://localhost:5173)

Frontend → Backend

During local development, the frontend sends requests to the FastAPI backend.

Example:

Frontend

[http://localhost:5173](http://localhost:5173)



        ↓



Backend

[http://127.0.0.1:8000/investigate](http://127.0.0.1:8000/investigate)

For production, the frontend should use the deployed backend API URL.

Deployment

The project can be deployed using separate frontend and backend services.

Backend

The FastAPI backend can be deployed on a platform such as Render.

Example start command:

uvicorn backend.api\:app --host 0.0.0.0 --port $PORT

Frontend

The React/Vite frontend can be deployed on a platform such as Vercel.

The frontend must be configured to use the production backend URL.

CORS

The FastAPI backend uses CORSMiddleware to allow requests from the frontend.

Configured origins should include the development frontend:

[http://localhost:5173](http://localhost:5173)

and the production frontend domain.

When deploying to a new frontend domain, update the allowed origins in:

backend/api.py

Testing

Before deployment, verify the backend locally.

Start the backend:

uvicorn backend.api\:app --reload

Then open:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Test:

POST /investigate

with:

{

  "claim": "The Earth revolves around the Sun."

}

Investigation State

The investigation workflow maintains a structured state containing information such as:

claim\_id

original\_claim

parsed\_claim

missing\_information

search\_queries\_used

search\_results

evidence

verification\_report

confidence

database\_matches

contradiction\_info

final\_decision

decision\_reasoning

investigation\_history

timestamps

errors

This allows different agents to contribute information throughout the investigation.

Design Principles

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

Future Improvements

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

Technology Stack

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

Knowledge / Storage

ChromaDB

SQLite

Deployment

Vercel

Render

Data & Storage

Application-generated data is stored locally during development.

The ChromaDB persistent storage is located under:

data/chroma/

The application database is managed by:

backend/database.py

Generated runtime data should generally not be committed to Git unless intentionally required by the project.

Troubleshooting

Backend does not start

Check that the virtual environment is activated:

.\venv\Scripts\Activate.ps1

Then reinstall dependencies:

pip install -r requirements.txt

Frontend does not start

Inside frontend/:

npm install

npm run dev

CORS error

Verify that the frontend URL is included in the allow\_origins list in:

backend/api.py

ChromaDB initialization error

Verify that backend/chroma\_db.py contains:

def initialize\_knowledge\_base():

and that backend/api.py imports it correctly:

from backend.chroma\_db import initialize\_knowledge\_base

API returns HTTP 500

Check the backend logs for the actual Python traceback.

The frontend's 500 Internal Server Error message alone does not identify the root cause.

👩‍💻 Development Workflow

Recommended workflow:

1\. Make code changes

        ↓

2\. Test locally

        ↓

3\. Check git status

        ↓

4\. Commit changes

        ↓

5\. Push to GitHub

        ↓

6\. Deploy backend/frontend

        ↓

7\. Test production API

        ↓

8\. Test production UI

Useful Git commands:

git status

git add .

git commit -m "Describe your changes"

git push origin main

📜 License

This project is currently developed as an academic/research project.

Add an appropriate open-source license if the project is later released publicly.

🎯 Project Goal

The goal of Sentinels of Truth is to demonstrate how multi-agent AI systems, evidence retrieval, structured reasoning, and persistent knowledge bases can be combined to build an explainable claim verification platform.

             ┌──────────────────────┐

             │      USER CLAIM      │

             └──────────┬───────────┘

                        ↓

             ┌──────────────────────┐

             │   CLAIM ANALYSIS     │

             └──────────┬───────────┘

                        ↓

             ┌──────────────────────┐

             │  EVIDENCE RETRIEVAL  │

             └──────────┬───────────┘

                        ↓

             ┌──────────────────────┐

             │   KNOWLEDGE BASE     │

             └──────────┬───────────┘

                        ↓

             ┌──────────────────────┐

             │ VERIFICATION AGENTS  │

             └──────────┬───────────┘

                        ↓

             ┌──────────────────────┐

             │ FINAL VERIFICATION   │

             │ + CONFIDENCE         │

             │ + REASONING          │

             │ + EVIDENCE           │

             └──────────────────────┘

Sentinels of Truth — Building reliable AI-assisted fact verification.

or should i submit this code, does it look ai generated