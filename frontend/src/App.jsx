import { useState } from "react";
import "./App.css";

function App() {
  const [claim, setClaim] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const verifyClaim = async () => {
    if (!claim.trim()) {
      setError("Please enter a claim.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/investigate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            claim: claim.trim(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Investigation failed. Server returned ${response.status}.`
        );
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the verification server."
      );
    } finally {
      setLoading(false);
    }
  };

  // Convert confidence from 0-1 to percentage
  const confidencePercent = result
    ? Math.round(Number(result.confidence || 0) * 100)
    : 0;

  // Safely read investigation history
  const history = Array.isArray(result?.investigation_history)
    ? result.investigation_history
    : [];

  // Decision CSS class
  const decisionClass = result?.decision
    ? result.decision.toLowerCase()
    : "unknown";

  // Agent status CSS class
  const getAgentStatusClass = (status) => {
    const normalizedStatus = String(status || "")
      .toLowerCase()
      .replace(/\s+/g, "_");

    if (
      normalizedStatus === "evidence_found" ||
      normalizedStatus === "match" ||
      normalizedStatus === "insert" ||
      normalizedStatus === "completed"
    ) {
      return "status-success";
    }

    if (
      normalizedStatus === "contradiction" ||
      normalizedStatus === "discard" ||
      normalizedStatus === "rejected"
    ) {
      return "status-danger";
    }

    if (
      normalizedStatus === "no_evidence" ||
      normalizedStatus === "flag" ||
      normalizedStatus === "unknown"
    ) {
      return "status-warning";
    }

    return "status-neutral";
  };

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="header">
        <div className="logo">S</div>

        <div>
          <h1>Sentinels of Truth</h1>
          <p>AI-powered claim verification system</p>
        </div>
      </header>


      {/* ================= MAIN ================= */}

      <main className="container">

        {/* ================= CLAIM INPUT ================= */}

        <section className="input-card">

          <h2>Verify a Claim</h2>

          <p className="subtitle">
            Enter a claim and let the verification agents investigate it.
          </p>

          <textarea
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Enter a claim to verify..."
            rows={6}
            disabled={loading}
          />

          <button
            onClick={verifyClaim}
            disabled={loading}
          >
            {loading
              ? "🔄 Investigating..."
              : "🔍 Verify Claim"}
          </button>

          {error && (
            <div className="error">
              <strong>Error:</strong> {error}
            </div>
          )}

        </section>


        {/* ================= LOADING ================= */}

        {loading && (
          <div className="loading-card">

            <div className="spinner"></div>

            <h3>Investigating claim...</h3>

            <p>
              AI agents are analyzing the claim and available evidence.
            </p>

          </div>
        )}


        {/* ================= RESULTS ================= */}

        {result && !loading && (
          <section className="result-card">

            {/* ================= RESULT HEADER ================= */}

            <div className="result-header">

              <div>
                <h2>Investigation Result</h2>

                <p>
                  Verification completed successfully
                </p>
              </div>

              <div className="success-icon">
                ✓
              </div>

            </div>


            {/* ================= DECISION + CONFIDENCE ================= */}

            <div className="result-grid">

              {/* Decision */}

              <div className="result-box">

                <span className="label">
                  DECISION
                </span>

                <span
                  className={`decision ${decisionClass}`}
                >
                  {result.decision || "UNKNOWN"}
                </span>

              </div>


              {/* Confidence */}

              <div className="result-box">

                <span className="label">
                  CONFIDENCE
                </span>

                <div className="confidence">

                  <div className="confidence-top">
                    <strong>
                      {confidencePercent}%
                    </strong>
                  </div>

                  <div className="progress">

                    <div
                      className="progress-fill"
                      style={{
                        width: `${confidencePercent}%`,
                      }}
                    ></div>

                  </div>

                </div>

              </div>

            </div>


            {/* ================= REASONING ================= */}

            <div className="reasoning">

              <span className="label">
                REASONING
              </span>

              <p>
                {result.reasoning ||
                  "No reasoning was provided."}
              </p>

            </div>


            {/* ================= AGENT PIPELINE ================= */}

            <div className="pipeline-section">

              <h3>
                🤖 Agent Investigation Pipeline
              </h3>

              <p className="pipeline-subtitle">
                Real-time execution history from the
                multi-agent verification system.
              </p>

              <div className="pipeline">

                {history.length > 0 ? (

                  history.map((item, index) => {

                    const agentName =
                      item?.agent?.toLowerCase() ||
                      "unknown";

                    const status =
                      item?.status || "UNKNOWN";

                    let displayName = "Unknown Agent";
                    let description = "Investigation step";

                    if (agentName === "alpha") {
                      displayName = "Alpha Agent";
                      description =
                        "Claim analysis & evidence discovery";
                    } else if (agentName === "beta") {
                      displayName = "Beta Agent";
                      description =
                        "Knowledge base verification & comparison";
                    } else if (agentName === "decision") {
                      displayName = "Decision Agent";
                      description =
                        "Final claim verdict generation";
                    }

                    const statusClass =
                      getAgentStatusClass(status);

                    return (
                      <div
                        key={`${agentName}-${index}`}
                      >

                        {/* Agent Card */}

                        <div
                          className={`agent-card ${statusClass}`}
                        >

                          <div className="agent-icon">
                            {statusClass === "status-danger"
                              ? "!"
                              : statusClass === "status-warning"
                              ? "!"
                              : "✓"}
                          </div>

                          <div className="agent-content">

                            <span className="agent-name">
                              {displayName}
                            </span>

                            <span className="agent-description">
                              {description}
                            </span>

                            <span className="agent-status">
                              {status}
                            </span>

                          </div>

                        </div>


                        {/* Pipeline Arrow */}

                        {index < history.length - 1 && (
                          <div className="pipeline-arrow">
                            ↓
                          </div>
                        )}

                      </div>
                    );
                  })

                ) : (

                  <div className="no-evidence">
                    No agent execution history was recorded.
                  </div>

                )}

              </div>

            </div>


            {/* ================= INVESTIGATION DETAILS ================= */}

            <div className="details-section">

              <h3>
                🔎 Investigation Details
              </h3>

              <div className="details-grid">

                {/* Claim ID */}

                <div>

                  <span className="label">
                    CLAIM ID
                  </span>

                  <p>
                    {result.claim_id ||
                      "Not available"}
                  </p>

                </div>


                {/* Original Claim */}

                <div>

                  <span className="label">
                    ORIGINAL CLAIM
                  </span>

                  <p>
                    {result.claim ||
                      claim ||
                      "Not available"}
                  </p>

                </div>


                {/* Search Queries */}

                <div>

                  <span className="label">
                    SEARCH QUERIES
                  </span>

                  {Array.isArray(result.search_queries) &&
                  result.search_queries.length > 0 ? (

                    <ul>

                      {result.search_queries.map(
                        (query, index) => (

                          <li key={index}>
                            {typeof query === "string"
                              ? query
                              : JSON.stringify(query)}
                          </li>

                        )
                      )}

                    </ul>

                  ) : (

                    <p>
                      No search queries recorded.
                    </p>

                  )}

                </div>


                {/* Investigation History */}

                <div>

                  <span className="label">
                    INVESTIGATION HISTORY
                  </span>

                  {history.length > 0 ? (

                    <ul>

                      {history.map(
                        (item, index) => (

                          <li key={index}>

                            {typeof item === "string"
                              ? item
                              : `${item?.agent || "Unknown"} → ${
                                  item?.status || "UNKNOWN"
                                }`}

                          </li>

                        )
                      )}

                    </ul>

                  ) : (

                    <p>
                      No investigation history recorded.
                    </p>

                  )}

                </div>

              </div>

            </div>


            {/* ================= EVIDENCE ================= */}

            <div className="evidence-section">

              <h3>
                📚 Evidence
              </h3>

              {Array.isArray(result.evidence) &&
              result.evidence.length > 0 ? (

                result.evidence.map(
                  (item, index) => (

                    <div
                      className="evidence-card"
                      key={index}
                    >

                      <div className="evidence-header">

                        <strong>
                          Evidence {index + 1}
                        </strong>

                      </div>

                      <p>
                        {typeof item === "string"
                          ? item
                          : item?.text ||
                            item?.content ||
                            item?.evidence ||
                            item?.description ||
                            JSON.stringify(item)}
                      </p>

                    </div>

                  )
                )

              ) : (

                <p className="no-evidence">
                  No evidence was recorded.
                </p>

              )}

            </div>


            {/* ================= SEARCH RESULTS ================= */}

            {Array.isArray(result.search_results) &&
            result.search_results.length > 0 && (

              <div className="evidence-section">

                <h3>
                  🌐 Search Results
                </h3>

                {result.search_results.map(
                  (item, index) => (

                    <div
                      className="evidence-card"
                      key={index}
                    >

                      <div className="evidence-header">

                        <strong>
                          Source {index + 1}
                        </strong>

                      </div>

                      <p>
                        {typeof item === "string"
                          ? item
                          : item?.title ||
                            item?.snippet ||
                            item?.content ||
                            JSON.stringify(item)}
                      </p>

                    </div>

                  )
                )}

              </div>

            )}


            {/* ================= VERIFICATION REPORT ================= */}

            {result.verification_report &&
            typeof result.verification_report === "object" &&
            Object.keys(result.verification_report).length > 0 && (

              <div className="evidence-section">

                <h3>
                  📋 Verification Report
                </h3>

                <div className="evidence-card">

                  <pre>
                    {JSON.stringify(
                      result.verification_report,
                      null,
                      2
                    )}
                  </pre>

                </div>

              </div>

            )}

          </section>
        )}

      </main>


      {/* ================= FOOTER ================= */}

      <footer>
        Sentinels of Truth • Multi-Agent Verification System
      </footer>

    </div>
  );
}

export default App;