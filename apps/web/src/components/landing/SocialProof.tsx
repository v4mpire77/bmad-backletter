import React from 'react';

const SocialProof = () => {
  return (
    <section className="social-proof fade-in">
      <div className="social-proof-text">Trusted by forward-thinking UK legal firms</div>
      <div className="trust-indicators">
        <div className="trust-badge">
          <span className="trust-icon">🛡️</span>
          <span>ISO 27001 Compliant</span>
        </div>
        <div className="trust-badge">
          <span className="trust-icon">⚖️</span>
          <span>SRA Approved Technology</span>
        </div>
        <div className="trust-badge">
          <span className="trust-icon">🔒</span>
          <span>UK Data Residency</span>
        </div>
        <div className="trust-badge">
          <span className="trust-icon">✅</span>
          <span>99.9% Uptime SLA</span>
        </div>
      </div>
    </section>
  );
};

export default SocialProof;
