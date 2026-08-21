# Sentinels of Truth

## Multi-Agent Verification & Knowledge-Base System

Sentinels of Truth is a multi-agent fact-checking and knowledge-management system designed to verify unverified claims and maintain a persistent knowledge base.

The system uses two distinct agents:

* **Agent Alpha — Investigator:** researches and verifies incoming claims using external search/evidence.
* **Agent Beta — Archivist:** checks the verification report against the existing knowledge base and decides whether the information should be inserted, discarded, or flagged for human review.

The agents communicate through a manually defined state schema orchestrated using LangGraph.

---

## 1. Problem Statement

News agencies receive a continuous stream of claims from different sources. Before accepting a claim into a long-term knowledge base, the claim must be investigated and checked against information that is already stored.

The system therefore needs to:

1. Accept an unverified claim from a user.
2. Investigate the claim using external information.
3. Generate a verification report.
4. Compare the report with existing knowledge.
5. Insert genuinely new and verified information.
6. Discard redundant information.
7. Flag contradictory information for human review.

Sentinels of Truth implements this workflow using a multi-agent architecture.

---

## 2. System Architecture

```text
                         USER
                           |
                           v
                  +------------------+
                  |  React Frontend  |
                  +------------------+
                           |
                           | HTTP Request
                           v
                  +------------------+
                  |   FastAPI API    |
                  +------------------+
                           |
                           v
                  +------------------+
                  |    LangGraph     |
                  |  State Workflow  |
                  +------------------+
                           |
                           v
                +----------------------+
                |    Agent Alpha       |
                |    Investigator      |
                +----------------------+
                           |
                           | Search / Evidence
                           v
                    +-------------+
                    | Search Tool |
                    +-------------+
                           |
                           | Verification Report
                           v
                +----------------------+
                |     Agent Beta       |
                |      Archivist       |
                +----------------------+
                           |
                           v
                 +--------------------+
                 |   Knowledge Base   |
                 +--------------------+
                    /            \
                   /              \
                  v                v
              SQLite           ChromaDB
            Structured       Semantic Search
              Storage
```

### Main Flow

```text
Claim
  |
  v
Parse Claim
  |
  v
Identify Missing Information
  |
  v
Search External Evidence
  |
  v
Generate Verification Report
  |
  v
Agent Beta
  |
  +---- New & Verified ------> INSERT
  |
  +---- Redundant -----------> DISCARD
  |
  +---- Contradiction -------> FLAG
  |
  v
Final Verification Result
```

---

## 3. Multi-Agent Design

The system contains two distinct agents with separate responsibilities and tool access.

### Agent Alpha — Investigator

Agent Alpha acts as the research and verification agent.

#### Responsibilities

* Parse the incoming claim.
* Identify information required for verification.
* Determine missing information.
* Formulate search queries.
* Search external sources.
* Collect relevant evidence.
* Analyze the collected evidence.
* Produce a verification report.

#### Important Constraint

Agent Alpha does **not** directly write to the knowledge base.

Its responsibility ends with producing the verification report and passing the resulting state to Agent Beta.

---

### Agent Beta — Archivist

Agent Beta acts as the gatekeeper of the persistent knowledge base.

#### Responsibilities

* Receive Agent Alpha's verification report.
* Query the existing knowledge base.
* Check whether similar information already exists.
* Detect contradictions.
* Determine the appropriate database action.

Agent Beta can produce one of three outcomes:

```text
INSERT
DISCARD
FLAG
```

#### INSERT

Used when:

* The information is verified.
* The information is sufficiently new.
* No conflicting knowledge is found.

```text
Verification Report
        |
        v
Knowledge Base Check
        |
        v
No existing contradiction
        |
        v
      INSERT
```

#### DISCARD

Used when the information is already represented in the knowledge base and does not add meaningful new information.

```text
Verification Report
        |
        v
Knowledge Base Check
        |
        v
Existing matching information
        |
        v
     DISCARD
```

#### FLAG

Used when the new information contradicts existing knowledge.

```text
Verification Report
        |
        v
Knowledge Base Check
        |
        v
Contradiction detected
        |
        v
       FLAG
        |
        v
Human Review
```

---

## 4. State Schema

The agents communicate through a shared state object managed by LangGraph.

The state maintains the history of the investigation as it moves through the workflow.

A representative state structure is:

```python
class VerificationState(TypedDict):
    claim_id: str
    original_claim: str
    parsed_claim: dict
    missing_information: list
    search_queries_used: list
    search_results: list
    evidence: list
    verification_report: dict
    database_result: dict
    final_status: str
```

### State Flow

```text
                         VerificationState
                                |
                                v
                         Agent Alpha
                                |
              +-----------------+----------------+
              |                 |                |
              v                 v                v
        Parsed Claim      Search Results     Evidence
              |                 |                |
              +-----------------+----------------+
                                |
                                v
                    Verification Report
                                |
                                v
                         Agent Beta
                                |
                                v
                       Database Result
                                |
                                v
                         Final Status
```

The state allows information produced by one stage of the workflow to be passed to subsequent stages without requiring the agents to directly share implementation details.

---

## 5. Knowledge Base

The system uses persistent storage for maintaining fact-checking information.

### SQLite

SQLite is used for structured persistent information such as:

* Claim identifiers
* Claims
* Verification status
* Database decisions
* Timestamps
* Other structured metadata

SQLite provides persistent relational storage for the system.

### ChromaDB

ChromaDB is used as the vector knowledge base.

It supports semantic similarity searches so that the Archivist can determine whether a newly investigated claim is similar to information that has already been stored.

This helps the system handle claims that are phrased differently but refer to the same underlying information.

---

## 6. Verification Workflow

The complete workflow is:

### Step 1 — Claim Input

The user enters an unverified claim through the web interface.

```text
User
 |
 v
"Claim to verify"
```

### Step 2 — Claim Parsing

Agent Alpha analyzes the claim and extracts the information necessary for verification.

### Step 3 — Missing Information

Alpha determines whether additional information is required to properly investigate the claim.

### Step 4 — Search

Alpha formulates search queries and obtains external evidence using the available search tool.

### Step 5 — Evidence Analysis

The gathered information is used to produce a verification report.

The report contains the information required by the Archivist to make a knowledge-base decision.

### Step 6 — Knowledge-Base Check

Agent Beta receives the state containing the verification report.

Beta checks the existing knowledge base for related information.

### Step 7 — Database Decision

Beta selects one of the following:

```text
INSERT
DISCARD
FLAG
```

### Step 8 — Final Response

The result is returned through the FastAPI backend to the frontend and displayed to the user.

---

## 7. Database Decision Logic

```text
                    Verification Report
                            |
                            v
                    Agent Beta checks
                    existing knowledge
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        New & Verified   Redundant    Contradiction
             |              |              |
             v              v              v
          INSERT         DISCARD          FLAG
             |              |              |
             +--------------+--------------+
                            |
                            v
                     Final Result
```

This prevents Agent Alpha from directly modifying long-term knowledge.

Only the Archivist is responsible for deciding how verified information should affect the knowledge base.

---

## 8. Technology Stack

### Frontend

* React
* Vite
* JavaScript / TypeScript
* CSS

### Backend

* Python
* FastAPI
* LangGraph

### Agents / AI

* Multi-agent workflow
* Agent Alpha — Investigator
* Agent Beta — Archivist
* Search-based evidence gathering

### Databases

* SQLite
* ChromaDB

### Development Tools

* Git
* GitHub
* npm
* Python virtual environment

---

## 9. Project Structure

```text
sentinels-of-truth/
│
├── backend/
│   ├── api.py
│   ├── database.py
│   ├── chroma_db.py
│   ├── graph.py
│   │
│   ├── agents/
│   │   ├── alpha.py
│   │   └── beta.py
│   │
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── data/
│   └── ...
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 10. Local Setup

### Prerequisites

Install:

* Python 3.x
* Node.js
* npm
* Git

---

### Clone the Repository

```bash
git clone https://github.com/MILI-5/sentinels-of-truth.git
cd sentinels-of-truth
```

---

## 11. Backend Setup

Create and activate a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

If the application requires API keys for external services, create a `.env` file in the appropriate location.

Do not commit API keys or other secrets to GitHub.

Example:

```text
SEARCH_API_KEY=your_api_key
LLM_API_KEY=your_api_key
```

Use the environment variable names expected by the implementation.

---

## 12. Initialize the Backend

The application initializes the required persistent storage during startup.

The startup sequence is:

```text
FastAPI starts
     |
     v
SQLite initialized
     |
     v
Knowledge Base initialized
     |
     v
API becomes available
```

The database initialization is handled by the backend rather than requiring the user to manually create database tables.

---

## 13. Run the Backend

From the project root:

```bash
uvicorn backend.api:app --reload
```

The FastAPI backend will then be available locally.

---

## 14. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Run the development server:

```bash
npm run dev
```

Open the local URL displayed by Vite.

---

## 15. Using the Application

### Step 1

Open the Sentinels of Truth web application.

### Step 2

Enter a claim into the input field.

Example:

```text
What revolves around the Sun?
```

### Step 3

Click:

```text
Verify Claim
```

### Step 4

The request is sent to the FastAPI backend.

### Step 5

Agent Alpha investigates the claim.

### Step 6

Agent Beta checks the existing knowledge base.

### Step 7

The application returns the verification result and database decision.

---

## 16. Example Outcomes

### New Information

```text
Verification Status: VERIFIED
Database Action: INSERTED
```

The information is considered new and is added to the knowledge base.

### Redundant Information

```text
Verification Status: REDUNDANT
Database Action: DISCARDED
```

The information already exists or is sufficiently similar to existing knowledge.

### Contradictory Information

```text
Verification Status: CONFLICT
Database Action: FLAGGED
```

The information conflicts with existing knowledge and is not automatically accepted.

---

## 17. API

The backend exposes an investigation endpoint used by the frontend.

### Investigation

```text
POST /investigate
```

The endpoint receives a claim and executes the multi-agent verification workflow.

Conceptually:

```text
POST /investigate
       |
       v
  LangGraph
       |
       v
 Agent Alpha
       |
       v
Verification Report
       |
       v
 Agent Beta
       |
       v
Database Decision
       |
       v
API Response
```

---

## 18. Separation of Agent Responsibilities

A key design principle of the project is that the agents do not have identical responsibilities.

| Component   | Responsibility                       |
| ----------- | ------------------------------------ |
| Frontend    | Accept claim and display result      |
| FastAPI     | API and application interface        |
| LangGraph   | Orchestrate agent workflow           |
| Agent Alpha | Investigation and evidence gathering |
| Search Tool | Retrieve external information        |
| Agent Beta  | Knowledge-base validation            |
| SQLite      | Structured persistent storage        |
| ChromaDB    | Semantic knowledge search            |

Agent Alpha produces evidence and a verification report.

Agent Beta is responsible for deciding whether the information should modify the knowledge base.

---

## 19. Assignment Requirement Mapping

| Assignment Requirement           | Implementation                      |
| -------------------------------- | ----------------------------------- |
| Web application                  | React frontend                      |
| User claim input                 | Claim input interface               |
| Multi-agent system               | Agent Alpha + Agent Beta            |
| Agent Alpha                      | Investigator                        |
| Agent Alpha search tool          | External/mock search functionality  |
| Agent Alpha database restriction | Alpha does not directly write to KB |
| Agent Beta                       | Archivist                           |
| Agent Beta database tools        | SQLite + ChromaDB                   |
| New verified information         | INSERT                              |
| Contradictory information        | FLAG                                |
| Redundant information            | DISCARD                             |
| Persistent storage               | SQLite                              |
| Semantic similarity              | ChromaDB                            |
| Agent orchestration              | LangGraph                           |
| Manual state schema              | `VerificationState`                 |
| State passed between agents      | LangGraph workflow                  |

---

## 20. Design Principles

### Separation of Concerns

Each component has a specific responsibility.

### Controlled Knowledge Updates

The knowledge base is not automatically updated simply because a claim was received.

### Persistent Memory

Verified information can be retained for future investigations.

### Semantic Comparison

ChromaDB allows the system to compare claims based on semantic similarity rather than relying only on exact text matching.

### Conflict Awareness

Contradictions are not silently overwritten. They are flagged for further review.

### Stateful Agent Workflow

The investigation history is maintained through the shared state object.

---

## 21. Deployment

The application can be deployed using separate frontend and backend services.

Typical deployment architecture:

```text
                   Internet
                      |
                      v
              +---------------+
              | Vercel        |
              | React Frontend|
              +---------------+
                      |
                      | HTTPS API
                      v
              +---------------+
              | Render        |
              | FastAPI       |
              +---------------+
                      |
                      v
              SQLite / ChromaDB
```

---

## 22. Live Demo

**Frontend:**
https://sentinels-of-truth-one.vercel.app/

**Backend:**
Add the deployed Render URL here.
https://sentinels-of-truth-1.onrender.com/

---

## 23. Demo Scenarios

For demonstrating the system, the following scenarios should be tested:

### Scenario 1 — New Claim

Submit a claim that is not already present in the knowledge base.

Expected result:

```text
INSERT
```

### Scenario 2 — Repeated Claim

Submit the same or a semantically equivalent claim again.

Expected result:

```text
DISCARD
```

### Scenario 3 — Conflicting Claim

Submit a claim that conflicts with existing knowledge.

Expected result:

```text
FLAG
```

These scenarios demonstrate the core behavior required by the assignment.

---

## 24. Future Improvements

Possible future improvements include:

* Human review interface for flagged conflicts.
* Source credibility scoring.
* More sophisticated contradiction detection.
* Additional search providers.
* PostgreSQL for production-scale relational storage.
* Improved vector retrieval and reranking.
* Source citation management.
* Authentication and role-based access.
* Monitoring and agent-level observability.
* Automated evaluation datasets.

---

## 25. Conclusion

Sentinels of Truth demonstrates a multi-agent approach to automated claim verification and knowledge management.

The system separates investigation from knowledge-base management:

```text
Agent Alpha
    |
    | Investigates
    v
Verification Report
    |
    v
Agent Beta
    |
    | Checks existing knowledge
    v
+---------+---------+
|         |         |
v         v         v
INSERT   DISCARD   FLAG
```

This architecture allows new verified information to be incorporated into persistent memory while preventing redundant or contradictory information from being silently accepted.

The project therefore provides a practical implementation of a **Multi-Agent Verification & Knowledge-Base System** using LangGraph, FastAPI, SQLite, ChromaDB, and a web-based user interface.
