import React from 'react';

const HowItWorks = () => {
  return (
    <section className="how-it-works" id="how-it-works">
      <div className="section-header">
        <h2>How it works</h2>
      </div>

      <div className="steps-grid">
        <div className="step-card fade-in stagger-1">
          <div className="step-number">1</div>
          <h3>Upload</h3>
          <p>Drop in a vendor DPA or lease (PDF/DOCX).</p>
        </div>

        <div className="step-card fade-in stagger-2">
          <div className="step-number">2</div>
          <h3>Detect</h3>
          <p>We run eight GDPR Article 28(3) checks using rulepacks + weak-language patterns.</p>
        </div>

        <div className="step-card fade-in stagger-3">
          <div className="step-number">3</div>
          <h3>Review</h3>
          <p>See Pass / Weak / Missing with snippet and rule ID. Filter by verdict.</p>
        </div>

        <div className="step-card fade-in stagger-4">
          <div className="step-number">4</div>
          <h3>Export</h3>
          <p>Generate a shareable report for stakeholders.</p>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
