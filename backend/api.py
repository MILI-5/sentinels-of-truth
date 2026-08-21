import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.database import (
    initialize_database,
    database_health_check,
)
from backend.graph import investigation_graph
from backend.models import InvestigationRequest, InvestigationResponse


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Sentinels of Truth",
    description="Multi-Agent Claim Verification System",
    version="1.0.0",
)


# Initialize SQLite database when the API starts
initialize_database()


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://sentinels-of-truth-one.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Sentinels of Truth API is running."
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# DATABASE HEALTH CHECK
# ============================================================

@app.get("/database-health")
def database_health():
    return database_health_check()


# ============================================================
# INVESTIGATE CLAIM
# ============================================================

@app.post(
    "/investigate",
    response_model=InvestigationResponse
)
def investigate(request: InvestigationRequest):

    if not request.claim or not request.claim.strip():
        raise HTTPException(
            status_code=400,
            detail="Claim cannot be empty."
        )

    initial_state = {
        "claim_id": f"api_{uuid.uuid4().hex[:12]}",
        "original_claim": request.claim.strip(),

        "parsed_claim": {},
        "missing_information": [],
        "search_queries_used": [],
        "search_results": [],
        "evidence": [],
        "verification_report": {},

        "confidence": 0.0,

        "database_matches": [],
        "contradiction_info": {},

        "final_decision": None,
        "decision_reasoning": None,

        "investigation_history": [],
        "timestamps": {},

        "errors": [],
    }

    try:
        result = investigation_graph.invoke(initial_state)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {str(exc)}"
        ) from exc

    return {
        "claim_id": result.get("claim_id"),

        "claim": result.get("original_claim"),

        "decision": result.get("final_decision"),

        "confidence": result.get("confidence", 0.0),

        "reasoning": result.get("decision_reasoning"),

        "evidence": result.get("evidence", []),

        "search_results": result.get(
            "search_results",
            []
        ),

        "search_queries": result.get(
            "search_queries_used",
            []
        ),

        "verification_report": result.get(
            "verification_report",
            {}
        ),

        "database_matches": result.get(
            "database_matches",
            []
        ),

        "contradiction_info": result.get(
            "contradiction_info",
            {}
        ),

        "investigation_history": result.get(
            "investigation_history",
            []
        ),

        "errors": result.get(
            "errors",
            []
        ),
    }