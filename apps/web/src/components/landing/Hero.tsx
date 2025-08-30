import React from 'react';

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-badge fade-in">Old rules. New game.</div>
      <h1 className="fade-in stagger-1">The AI legal assistant built for UK compliance</h1>
      <p className="fade-in stagger-2">
        Cut contract review time by 60% and never miss a GDPR obligation. Blackletter flags Article 28(3) clause gaps with explainable findings — snippet, rule ID, and rationale.
      </p>
      <div className="cta-buttons fade-in stagger-3">
        <a href="/new" className="btn-primary" aria-label="Start free trial of GDPR Checker">Start Free 14-Day Trial</a>
        <a href="/dashboard" className="btn-secondary" aria-label="View interactive demo dashboard">Watch Interactive Demo</a>
      </div>
      <div className="hero-micro fade-in stagger-4">
        Private by default. LLM is off unless you enable it. When enabled, we only send short snippets.
      </div>
    </section>
  );
};

export default Hero;
