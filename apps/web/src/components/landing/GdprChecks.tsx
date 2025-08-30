import React from 'react';

const GdprChecks = () => {
  return (
    <section className="gdpr-checks">
      <div className="section-header">
        <h2>Eight core checks, mapped to GDPR Article 28(3)</h2>
      </div>

      <div className="checks-container fade-in">
        <div className="checks-grid">
          <div className="check-pill">Instructions</div>
          <div className="check-pill">Confidentiality</div>
          <div className="check-pill">Security (Art.32)</div>
          <div className="check-pill">Sub-processors & flow-down</div>
          <div className="check-pill">Data-subject rights assistance</div>
          <div className="check-pill">Breach notice</div>
          <div className="check-pill">Return/Delete</div>
          <div className="check-pill">Audits & information</div>
        </div>

        <div className="metrics-bar">
          <div className="metric">
            <div className="metric-content">
              <span className="metric-value">p95 ≤ 60s / document</span>
              <div className="metric-label">Speed target</div>
            </div>
          </div>
          <div className="metric">
            <div className="metric-content">
              <span className="metric-value">Explainability ≥ 95%</span>
              <div className="metric-label">Clarity target</div>
            </div>
          </div>
          <div className="metric">
            <div className="metric-content">
              <span className="metric-value">Cost ~ £0.10 / document</span>
              <div className="metric-label">Pricing target</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default GdprChecks;
