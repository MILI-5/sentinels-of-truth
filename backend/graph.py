from langgraph.graph import StateGraph, START, END

from backend.state import InvestigationState

from backend.agents.alpha import investigate_claim
from backend.agents.beta import investigate_knowledge_base

from backend.decision import decide_action

from backend.action import (
    execute_insert,
    execute_flag,
    execute_discard,
)


DISTANCE_THRESHOLD = 1.0


def calculate_confidence(
    evidence: list[dict],
    distance_threshold: float,
) -> float:
    """Convert ChromaDB distance into a confidence score."""

    if not evidence:
        return 0.0

    best_distance = evidence[0].get(
        "distance"
    )

    if best_distance is None:
        return 0.0

    if distance_threshold <= 0:
        return 0.0

    confidence = (
        1.0
        - (
            best_distance
            / distance_threshold
        )
    )

    return round(
        max(
            0.0,
            min(1.0, confidence)
        ),
        2,
    )


def alpha_node(
    state: InvestigationState,
):
    """Run Agent Alpha."""

    print("\n[Alpha Node] Running...")

    claim = state["original_claim"]

    alpha_result = investigate_claim(
        claim=claim,
        n_results=5,
        distance_threshold=DISTANCE_THRESHOLD,
    )

    confidence = calculate_confidence(
        alpha_result["evidence"],
        DISTANCE_THRESHOLD,
    )

    print(
        "[Alpha Node] Status:",
        alpha_result["status"],
    )

    print(
        "[Alpha Node] Evidence:",
        alpha_result["evidence_count"],
    )

    return {
        "search_results": (
            alpha_result["search_results"]
        ),

        "search_queries_used": (
            alpha_result["search_queries"]
        ),

        "evidence": (
            alpha_result["evidence"]
        ),

        "verification_report": {
            "status": alpha_result["status"],

            "evidence_count": (
                alpha_result["evidence_count"]
            ),

            "best_evidence": (
                alpha_result["best_evidence"]
            ),
        },

        "confidence": confidence,

        "investigation_history": [
            {
                "agent": "alpha",
                "status": alpha_result["status"],
            }
        ],
    }


def beta_node(
    state: InvestigationState,
):
    """Run Agent Beta."""

    print("\n[Beta Node] Running...")

    claim = state["original_claim"]

    beta_result = investigate_knowledge_base(
        claim
    )

    print(
        "[Beta Node] Status:",
        beta_result["comparison_status"],
    )

    return {
        "database_matches": (
            beta_result["database_matches"]
        ),

        "contradiction_info": (
            beta_result["contradiction_info"]
        ),

        "investigation_history": (
            state["investigation_history"]
            + [
                {
                    "agent": "beta",
                    "status": (
                        beta_result[
                            "comparison_status"
                        ]
                    ),
                }
            ]
        ),
    }


def decision_node(
    state: InvestigationState,
):
    """Generate and execute the final decision."""

    print("\n[Decision Node] Running...")

    alpha_status = (
        state[
            "verification_report"
        ].get(
            "status",
            "NO_EVIDENCE",
        )
    )

    beta_status = (
        state[
            "investigation_history"
        ][-1]["status"]
    )

    decision_result = decide_action(
        alpha_status=alpha_status,
        beta_status=beta_status,
    )

    decision = decision_result[
        "decision"
    ]

    reason = decision_result[
        "reason"
    ]

    print(
        "[Decision Node] Decision:",
        decision,
    )

    if decision == "INSERT":

        action_result = execute_insert(
            claim_id=state["claim_id"],
            claim=state["original_claim"],
            confidence=state["confidence"],
            evidence=state["evidence"],
            reasoning=reason,
        )

    elif decision == "FLAG":

        action_result = execute_flag(
            claim_id=state["claim_id"],
            claim=state["original_claim"],
            reason=reason,
        )

    else:

        action_result = execute_discard(
            claim_id=state["claim_id"],
            claim=state["original_claim"],
            reason=reason,
        )

    print(
        "[Decision Node] Action:",
        action_result["action"],
    )

    print(
        "[Decision Node] Action Status:",
        action_result["status"],
    )

    return {
        "final_decision": decision,

        "decision_reasoning": reason,

        "investigation_history": (
            state["investigation_history"]
            + [
                {
                    "agent": "decision",
                    "status": decision,
                }
            ]
        ),
    }


def route_after_alpha(
    state: InvestigationState,
):
    """Route Alpha to Beta."""

    status = (
        state[
            "verification_report"
        ].get(
            "status",
            "NO_EVIDENCE",
        )
    )

    print(
        f"\n[Router] Alpha status: {status}"
    )

    print(
        "[Router] Routing to Beta..."
    )

    return "beta"


builder = StateGraph(
    InvestigationState
)


builder.add_node(
    "alpha",
    alpha_node,
)

builder.add_node(
    "beta",
    beta_node,
)

builder.add_node(
    "decision",
    decision_node,
)


builder.add_edge(
    START,
    "alpha",
)

builder.add_conditional_edges(
    "alpha",
    route_after_alpha,
    {
        "beta": "beta",
    },
)

builder.add_edge(
    "beta",
    "decision",
)

builder.add_edge(
    "decision",
    END,
)


investigation_graph = builder.compile()


if __name__ == "__main__":

    print(
        "LangGraph created successfully."
    )

    initial_state = {

        "claim_id":
            "test_claim_001",

        "original_claim":
            "The Earth revolves around the Sun.",

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

    result = investigation_graph.invoke(
        initial_state
    )

    print(
        "\nGraph execution completed."
    )

    print(
        "\nFinal State:"
    )

    print(result)