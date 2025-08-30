import React from 'react';

const WhyBlackletter = () => {
  return (
    <section className="why-blackletter">
      <div className="section-header">
        <h2>Why Blackletter</h2>
      </div>

      <div className="features-grid">
        <div className="feature-card fade-in stagger-1">
          <div className="feature-icon" aria-hidden="true">⚖️</div>
          <h3>Compliance-first, not generic AI</h3>
          <p>Purpose-built for UK GDPR and SRA expectations — built to reduce risk, not just speed up text.</p>
        </div>

        <div className="feature-card fade-in stagger-2">
          <div className="feature-icon" aria-hidden="true">🔍</div>
          <h3>Explainable by design</h3>
          <p>Every finding shows the clause snippet, detector rule ID, and short why so reviewers can validate quickly.</p>
        </div>

        <div className="feature-card fade-in stagger-3">
          <div className="feature-icon" aria-hidden="true">📋</div>
          <h3>Auditable outputs</h3>
          <p>Export a clean report (PDF/HTML) with findings, snippets, and timestamps — ready for internal sign-off or vendor follow-up.</p>
        </div>

        <div className="feature-card fade-in stagger-4">
          <div className="feature-icon" aria-hidden="true">💰</div>
          <h3>Token-disciplined, cost-controlled</h3>
          <p>LLM usage is optional and snippet-only with hard caps. Deterministic rules do the heavy lifting.</p>
        </div>

        <div className="feature-card fade-in stagger-5">
          <div className="feature-icon" aria-hidden="true">🏢</div>
          <h3>Built for UK SMEs</h3>
          <p>Designed for 10–200 fee-earner firms. Windows-friendly development with a simple path to scale.</p>
        </div>
      </div>
    </section>
  );
};

export default WhyBlackletter;
