'use client';

import React, { useState, useEffect, useCallback, memo } from 'react';
import Link from 'next/link';

const LandingPage = memo(function LandingPage() {
  const [isDarkTheme, setIsDarkTheme] = useState(true);
  const [isScrolled, setIsScrolled] = useState(false);

  const toggleTheme = useCallback(() => {
    setIsDarkTheme(prev => !prev);
  }, []);

  useEffect(() => {
    // Apply theme to body
    if (isDarkTheme) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }, [isDarkTheme]);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    // Throttle scroll events for better performance
    let ticking = false;
    const throttledScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          handleScroll();
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', throttledScroll, { passive: true });

    // Initialize fade-in animations
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach((el, index) => {
      setTimeout(() => {
        (el as HTMLElement).style.opacity = '1';
        (el as HTMLElement).style.transform = 'translateY(0)';
      }, index * 100);
    });

    // Smooth scrolling for anchor links
    const handleAnchorClick = (e: Event) => {
      e.preventDefault();
      const href = (e.currentTarget as HTMLAnchorElement).getAttribute('href');
      const target = document.querySelector(href || '');
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    };

    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach(anchor => {
      anchor.addEventListener('click', handleAnchorClick);
    });

    return () => {
      window.removeEventListener('scroll', throttledScroll);
      anchors.forEach(anchor => {
        anchor.removeEventListener('click', handleAnchorClick);
      });
    };
  }, []);

  return (
    <>
      {/* Background Elements */}
      <div className="bg-elements">
        <div className="floating-gradient gradient-1"></div>
        <div className="floating-gradient gradient-2"></div>
        <div className="floating-gradient gradient-3"></div>
      </div>

      {/* Navigation */}
      <nav className={isScrolled ? 'scrolled' : ''} id="navbar">
        <div className="nav-container">
          <div className="logo">Blackletter Systems</div>
          <ul className="nav-links">
            <li><a href="#how-it-works">How it works</a></li>
            <li><a href="#faq">FAQ</a></li>
          </ul>
          <button className="theme-toggle" onClick={toggleTheme}>
            <span id="theme-icon">{isDarkTheme ? '☀️ Light' : '🌙 Dark'}</span>
          </button>
        </div>
      </nav>

      <div className="container">
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-badge fade-in">Old rules. New game.</div>
          <h1 className="fade-in stagger-1">The AI legal assistant built for UK compliance</h1>
          <p className="fade-in stagger-2">
            Cut contract review time by 60% and never miss a GDPR obligation. Blackletter flags Article 28(3) clause gaps with explainable findings — snippet, rule ID, and rationale.
          </p>
          <div className="cta-buttons fade-in stagger-3">
            <Link href="/new" className="btn-primary" aria-label="Start free trial of GDPR Checker">
              Start Free 14-Day Trial
            </Link>
            <Link href="/dashboard" className="btn-secondary" aria-label="Try the Blackletter demo dashboard">
              Try the Demo
            </Link>
          </div>
          <div className="hero-micro fade-in stagger-4">
            Private by default. LLM is off unless you enable it. When enabled, we only send short snippets.
          </div>
        </section>

        {/* Social Proof Section */}
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

        {/* Why Blackletter Section */}
        <section className="why-blackletter">
          <div className="section-header">
            <h2>Why Blackletter</h2>
          </div>
          
          <div className="features-grid">
            <div className="feature-card fade-in stagger-1">
              <h3>Compliance-first, not generic AI</h3>
              <p>Purpose-built for UK GDPR and SRA expectations — built to reduce risk, not just speed up text.</p>
            </div>
            
            <div className="feature-card fade-in stagger-2">
              <h3>Explainable by design</h3>
              <p>Every finding shows the clause snippet, detector rule ID, and short why so reviewers can validate quickly.</p>
            </div>
            
            <div className="feature-card fade-in stagger-3">
              <h3>Auditable outputs</h3>
              <p>Export a clean report (PDF/HTML) with findings, snippets, and timestamps — ready for internal sign-off or vendor follow-up.</p>
            </div>
            
            <div className="feature-card fade-in stagger-4">
              <h3>Token-disciplined, cost-controlled</h3>
              <p>LLM usage is optional and snippet-only with hard caps. Deterministic rules do the heavy lifting.</p>
            </div>
            
            <div className="feature-card fade-in stagger-5">
              <h3>Built for UK SMEs</h3>
              <p>Designed for 10–200 fee-earner firms. Windows-friendly development with a simple path to scale.</p>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
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

        {/* GDPR Checks Section */}
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
      </div>
    </>
  );
});

export default LandingPage;
