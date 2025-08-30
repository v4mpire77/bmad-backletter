"use client";

import { useEffect } from 'react';

export default function NewLandingPage() {
  useEffect(() => {
    // Theme Toggle
    function toggleTheme() {
        const body = document.body;
        const themeIcon = document.getElementById('theme-icon');

        if (body.classList.contains('dark-theme')) {
            body.classList.remove('dark-theme');
            if (themeIcon) themeIcon.textContent = '🌙 Dark';
        } else {
            body.classList.add('dark-theme');
            if (themeIcon) themeIcon.textContent = '☀️ Light';
        }
    }

    const themeToggleButton = document.querySelector('.theme-toggle');
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', toggleTheme);
    }


    // Navbar scroll effect
    const handleScroll = () => {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    };
    window.addEventListener('scroll', handleScroll);

    // Smooth scrolling for navigation links
    const smoothScroll = (e: Event) => {
        e.preventDefault();
        const targetId = (e.currentTarget as HTMLAnchorElement).getAttribute('href');
        if (targetId) {
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    };

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', smoothScroll);
    });

    // Initialize animations on load
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach((el, index) => {
        setTimeout(() => {
            (el as HTMLElement).style.opacity = '1';
            (el as HTMLElement).style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Set initial theme
    const themeIcon = document.getElementById('theme-icon');
    if(themeIcon) themeIcon.textContent = '☀️ Light';


    return () => {
        if (themeToggleButton) {
            themeToggleButton.removeEventListener('click', toggleTheme);
        }
        window.removeEventListener('scroll', handleScroll);
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.removeEventListener('click', smoothScroll);
        });
    };
  }, []);

  return (
    <>
        <style dangerouslySetInnerHTML={{ __html: `
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            /* Light theme colors */
            --primary-bg: #fafafa;
            --secondary-bg: #ffffff;
            --card-bg: #ffffff;
            --accent-gold: #c9a961;
            --accent-gold-light: #d4b36a;
            --text-primary: #1a1a1a;
            --text-secondary: #4a4a4a;
            --text-muted: #888888;
            --border-color: rgba(0, 0, 0, 0.1);
            --gradient-primary: linear-gradient(135deg, #c9a961 0%, #d4b36a 100%);
            --shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            --shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.12);
        }

        .dark-theme {
            /* Enhanced dark theme colors */
            --primary-bg: #0f0f0f;
            --secondary-bg: #1a1a1a;
            --card-bg: #242424;
            --accent-gold: #f4d03f;
            --accent-gold-light: #f7dc6f;
            --text-primary: #ffffff;
            --text-secondary: #b8b8b8;
            --text-muted: #6b6b6b;
            --border-color: rgba(255, 255, 255, 0.1);
            --gradient-primary: linear-gradient(135deg, #f4d03f 0%, #f7dc6f 100%);
            --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            --shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.4);
        }

        /* Enhanced typography and readability */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: var(--primary-bg);
            color: var(--text-primary);
            line-height: 1.75;
            transition: all 0.3s ease;
        }

        /* Improved focus indicators for accessibility */
        *:focus {
            outline: 2px solid var(--accent-gold);
            outline-offset: 2px;
        }

        button:focus, a:focus {
            outline: 2px solid var(--accent-gold);
            outline-offset: 2px;
        }

        /* Floating Background Elements */
        .bg-elements {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.3;
        }

        .floating-gradient {
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.1;
            animation: float 25s ease-in-out infinite;
        }

        .gradient-1 {
            width: 500px;
            height: 500px;
            background: var(--gradient-primary);
            top: 10%;
            left: -10%;
            animation-delay: 0s;
        }

        .gradient-2 {
            width: 400px;
            height: 400px;
            background: var(--gradient-primary);
            top: 40%;
            right: -15%;
            animation-delay: 10s;
        }

        .gradient-3 {
            width: 300px;
            height: 300px;
            background: var(--gradient-primary);
            bottom: 10%;
            left: 20%;
            animation-delay: 20s;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) scale(1) rotate(0deg); }
            33% { transform: translateY(-40px) scale(1.1) rotate(5deg); }
            66% { transform: translateY(30px) scale(0.9) rotate(-5deg); }
        }

        /* Navigation */
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            padding: 1.5rem 2rem;
            transition: all 0.3s ease;
        }

        nav.scrolled {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-color);
        }

        .dark-theme nav.scrolled {
            background: rgba(15, 15, 15, 0.95);
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1400px;
            margin: 0 auto;
        }

        .logo {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: color 0.3s ease;
            position: relative;
        }

        .nav-links a:hover {
            color: var(--accent-gold);
        }

        .theme-toggle {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            box-shadow: var(--shadow);
        }

        .theme-toggle:hover {
            border-color: var(--accent-gold);
            box-shadow: var(--shadow-hover);
            transform: translateY(-1px);
        }

        /* Main Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 8rem 2rem 2rem;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            margin-bottom: 8rem;
        }

        .hero-badge {
            display: inline-block;
            padding: 0.6rem 1.5rem;
            background: rgba(244, 208, 63, 0.15);
            border: 1px solid rgba(244, 208, 63, 0.3);
            border-radius: 25px;
            color: var(--accent-gold);
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 2rem;
            letter-spacing: 0.5px;
        }

        .hero h1 {
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 3rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        .cta-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }

        .btn-primary {
            padding: 1.2rem 2.5rem;
            background: var(--gradient-primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            box-shadow: var(--shadow);
            min-height: 48px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        .btn-primary::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .btn-primary:hover::before {
            left: 100%;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(244, 208, 63, 0.4);
        }

        .btn-secondary {
            padding: 1.2rem 2.5rem;
            background: var(--card-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow);
            min-height: 48px;
        }

        .btn-secondary:hover {
            border-color: var(--accent-gold);
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }

        .hero-micro {
            margin-top: 2rem;
            font-size: 0.9rem;
            color: var(--text-muted);
            font-style: italic;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Section Headers */
        .section-header {
            text-align: left;
            margin-bottom: 3rem;
        }

        .section-header h2 {
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }

        /* Why Blackletter Section */
        .why-blackletter {
            margin-bottom: 6rem;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }

        @media (max-width: 1024px) {
            .features-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .features-grid {
                grid-template-columns: 1fr;
            }
        }

        .feature-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }

        .feature-icon {
            width: 48px;
            height: 48px;
            background: var(--gradient-primary);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(244, 208, 63, 0.3);
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--gradient-primary);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .feature-card:hover::before {
            transform: scaleX(1);
        }

        .feature-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: var(--shadow-hover);
        }

        .feature-card:hover .feature-icon {
            transform: scale(1.1) rotate(5deg);
        }

        .feature-card h3 {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .feature-card p {
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* How It Works Section */
        .how-it-works {
            margin-bottom: 6rem;
        }

        .steps-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
        }

        @media (max-width: 1024px) {
            .steps-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .steps-grid {
                grid-template-columns: 1fr;
            }
        }

        .step-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow);
            text-align: left;
        }

        .step-card:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: var(--shadow-hover);
        }

        .step-card:hover .step-number {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(244, 208, 63, 0.4);
        }

        /* Progress indicator for steps */
        .step-card::after {
            content: '';
            position: absolute;
            top: 50%;
            right: -0.75rem;
            width: 1.5rem;
            height: 2px;
            background: var(--border-color);
            transform: translateY(-50%);
        }

        .step-card:last-child::after {
            display: none;
        }

        .step-number {
            display: inline-block;
            width: 32px;
            height: 32px;
            background: var(--gradient-primary);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: white;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }

        .step-card h3 {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
            color: var(--text-primary);
        }

        .step-card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        /* GDPR Checks Section */
        .gdpr-checks {
            margin-bottom: 6rem;
        }

        .checks-container {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: var(--shadow);
        }

        .checks-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .check-pill {
            background: rgba(244, 208, 63, 0.15);
            color: var(--accent-gold);
            padding: 0.6rem 1.2rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(244, 208, 63, 0.3);
        }

        .metrics-bar {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
        }

        .metric {
            text-align: left;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .metric::before {
            content: '●';
            color: var(--accent-gold);
            font-size: 0.8rem;
        }

        .metric-content {
            display: flex;
            flex-direction: column;
        }

        .metric-value {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            display: block;
        }

        .metric-label {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.1rem;
        }

        /* Social Proof Section */
        .social-proof {
            margin: 4rem 0;
            text-align: center;
            padding: 2rem;
            background: rgba(244, 208, 63, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(244, 208, 63, 0.15);
        }

        .social-proof-text {
            font-size: 0.95rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }

        .trust-indicators {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            flex-wrap: wrap;
        }

        .trust-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .trust-icon {
            color: var(--accent-gold);
            font-size: 1.1rem;
        }

        /* FAQ Section */
        .faq-section {
            margin: 6rem 0;
        }

        .faq-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }

        .faq-item {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
        }

        .faq-question {
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.8rem;
            font-size: 1.05rem;
        }

        .faq-answer {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* Footer */
        .footer {
            margin-top: 8rem;
            padding: 4rem 0 2rem;
            border-top: 1px solid var(--border-color);
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 3rem;
            margin-bottom: 3rem;
        }

        .footer-section h4 {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--accent-gold);
        }

        .footer-section ul {
            list-style: none;
        }

        .footer-section ul li {
            margin-bottom: 0.7rem;
        }

        .footer-section ul li a {
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.3s ease;
            font-size: 0.95rem;
        }

        .footer-section ul li a:hover {
            color: var(--accent-gold);
        }

        .footer-bottom {
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
        }

        .footer-disclaimer {
            margin-top: 1rem;
            font-size: 0.85rem;
            font-style: italic;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }

            .container {
                padding: 6rem 1rem 2rem;
            }

            .cta-buttons {
                flex-direction: column;
                align-items: center;
            }

            .btn-primary,
            .btn-secondary {
                width: 100%;
                max-width: 300px;
            }

            .features-grid,
            .steps-grid,
            .faq-grid {
                grid-template-columns: 1fr;
            }

            .metrics-bar {
                grid-template-columns: 1fr;
                gap: 1rem;
            }

            .trust-indicators {
                flex-direction: column;
                gap: 1rem;
            }

            .checks-grid {
                justify-content: center;
            }

            .step-card::after {
                display: none;
            }
        }

        /* Animation Classes */
        .fade-in {
            opacity: 0;
            transform: translateY(20px);
            animation: fadeIn 0.8s ease forwards;
        }

        @keyframes fadeIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .stagger-1 { animation-delay: 0.1s; }
        .stagger-2 { animation-delay: 0.2s; }
        .stagger-3 { animation-delay: 0.3s; }
        .stagger-4 { animation-delay: 0.4s; }
        .stagger-5 { animation-delay: 0.5s; }
        .stagger-6 { animation-delay: 0.6s; }
    `}} />
      {/* Background Elements */}
      <div className="bg-elements">
          <div className="floating-gradient gradient-1"></div>
          <div className="floating-gradient gradient-2"></div>
          <div className="floating-gradient gradient-3"></div>
      </div>

      {/* Navigation */}
      <nav id="navbar">
          <div className="nav-container">
              <div className="logo">Blackletter Systems</div>
              <ul className="nav-links">
                  <li><a href="#how-it-works">How it works</a></li>
                  <li><a href="#faq">FAQ</a></li>
              </ul>
              <button className="theme-toggle">
                  <span id="theme-icon">☀️ Light</span>
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
                  <a href="/new" className="btn-primary" aria-label="Start free trial of GDPR Checker">Start Free 14-Day Trial</a>
                  <a href="/dashboard" className="btn-secondary" aria-label="View interactive demo dashboard">Watch Interactive Demo</a>
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

          {/* FAQ Section */}
          <section className="faq-section" id="faq">
            <div className="section-header">
                <h2>Frequently Asked Questions</h2>
            </div>

            <div className="faq-grid">
                <div className="faq-item fade-in stagger-1">
                    <div className="faq-question">Is this a replacement for legal review?</div>
                    <div className="faq-answer">No. It's a speed and consistency layer — evidence-first findings to support professional judgement.</div>
                </div>

                <div className="faq-item fade-in stagger-2">
                    <div className="faq-question">What data leaves the browser?</div>
                    <div className="faq-answer">Your file is processed server-side. If you enable LLM, only short snippets are sent with token caps; otherwise processing stays rule-first.</div>
                </div>

                <div className="faq-item fade-in stagger-3">
                    <div className="faq-question">Which documents work best?</div>
                    <div className="faq-answer">Vendor DPAs, MSAs, and leases. PDF/DOCX up to 10MB.</div>
                </div>

                <div className="faq-item fade-in stagger-4">
                    <div className="faq-question">What's the pricing model?</div>
                    <div className="faq-answer">Early-access pricing from £50–100 per user/month. Volume discounts available for larger firms.</div>
                </div>

                <div className="faq-item fade-in stagger-5">
                    <div className="faq-question">How accurate are the findings?</div>
                    <div className="faq-answer">Our deterministic rules achieve 95%+ accuracy on core GDPR checks, with explainable rationale for every finding.</div>
                </div>

                <div className="faq-item fade-in stagger-6">
                    <div className="faq-question">Do you offer training and support?</div>
                    <div className="faq-answer">Yes. We provide comprehensive onboarding, training materials, and dedicated support for all users.</div>
                </div>
            </div>
        </section>

        {/* Footer */}
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-section">
                    <h4>Product</h4>
                    <ul>
                        <li><a href="/new">GDPR Checker</a></li>
                        <li><a href="/dashboard">Demo Dashboard</a></li>
                        <li><a href="/pricing">Pricing</a></li>
                        <li><a href="/features">All Features</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h4>Legal & Compliance</h4>
                    <ul>
                        <li><a href="/gdpr-guide">UK GDPR Guide</a></li>
                        <li><a href="/article-28-reference">Article 28(3) Reference</a></li>
                        <li><a href="/privacy">Privacy Policy</a></li>
                        <li><a href="/terms">Terms of Service</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h4>Resources</h4>
                    <ul>
                        <li><a href="/docs">Documentation</a></li>
                        <li><a href="/case-studies">Case Studies</a></li>
                        <li><a href="/support">Support</a></li>
                        <li><a href="#faq">FAQ</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="/about">About Us</a></li>
                        <li><a href="/contact">Contact</a></li>
                        <li><a href="/careers">Careers</a></li>
                        <li><a href="/security">Security</a></li>
                    </ul>
                </div>
            </div>
            <div className="footer-bottom">
                <p>&copy; 2025 Blackletter Systems. All rights reserved.</p>
                <div className="footer-disclaimer">
                    Blackletter Systems provides software for compliance support. It does not provide legal advice. Results require professional review.
                </div>
            </div>
        </footer>
      </div>
    </>
  );
}
