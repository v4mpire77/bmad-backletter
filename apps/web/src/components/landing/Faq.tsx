import React from 'react';

const Faq = () => {
  return (
    <section className="faq-section">
      <div className="section-header">
        <h2>Frequently Asked Questions</h2>
      </div>
      <div className="faq-grid">
        <div className="faq-item">
          <h3 className="faq-question">Is this a replacement for legal review?</h3>
          <p className="faq-answer">No. Blackletter is a tool to assist legal professionals by automating the detection of common compliance gaps. It is not a substitute for professional legal advice.</p>
        </div>
        <div className="faq-item">
          <h3 className="faq-question">Which documents work best?</h3>
          <p className="faq-answer">Vendor DPAs, leases, and other contracts that reference GDPR Article 28(3) obligations will have the highest detection accuracy.</p>
        </div>
        <div className="faq-item">
          <h3 className="faq-question">Do you use our data for training?</h3>
          <p className="faq-answer">No. We do not use customer data for training our models. All data is processed in-memory and deleted after the analysis is complete.</p>
        </div>
        <div className="faq-item">
          <h3 className="faq-question">Is the LLM feature secure?</h3>
          <p className="faq-answer">Yes. The LLM feature is optional and off by default. When enabled, we only send short, anonymized snippets of text to the model. We use a UK-based provider with a strict data privacy policy.</p>
        </div>
      </div>
    </section>
  );
};

export default Faq;
