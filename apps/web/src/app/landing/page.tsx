"use client";

import { useEffect } from "react";
import { landing } from "@/content/landing";

export default function LandingPage() {
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem("theme");
      const body = document.body;
      if (saved === "light") body.classList.add("light-theme");
    } catch {}

    const onScroll = () => {
      const navbar = document.getElementById("navbar");
      if (!navbar) return;
      if (window.scrollY > 100) navbar.classList.add("scrolled");
      else navbar.classList.remove("scrolled");
    };
    window.addEventListener("scroll", onScroll);
    onScroll();

    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => e.isIntersecting && e.target.classList.add("in-view"));
    }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });
    document.querySelectorAll(".animate-on-scroll").forEach((el) => io.observe(el));

    return () => {
      window.removeEventListener("scroll", onScroll);
      io.disconnect();
    };
  }, []);

  function toggleTheme() {
    const body = document.body;
    const toLight = !body.classList.contains("light-theme");
    if (toLight) {
      body.classList.add("light-theme");
      try { window.localStorage.setItem("theme", "light"); } catch {}
    } else {
      body.classList.remove("light-theme");
      try { window.localStorage.setItem("theme", "dark"); } catch {}
    }
  }

  return (
    <>
      <style>{`
        :root { --bg: #0b0b0c; --fg: #f7f7f8; --muted: #b3b3b7; --card: #121214; --accent: #0ea5e9; }
        .light-theme { --bg: #ffffff; --fg: #0b0b0c; --muted: #4b5563; --card: #f8fafc; }
        body { background: var(--bg); color: var(--fg); }
        a { color: inherit; }
        .container { max-width: 1120px; margin: 0 auto; padding: 0 1rem; }
        nav { position: sticky; top: 0; z-index: 40; background: rgba(11,11,12,0.6); backdrop-filter: blur(8px); border-bottom: 1px solid rgba(255,255,255,0.08); }
        nav.scrolled { background: rgba(11,11,12,0.9); }
        .logo { font-weight: 700; letter-spacing: 0.5px; }
        .theme-toggle { border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 6px 10px; }
        .hero { padding: 80px 0 48px; text-align: center; }
        .hero-badge { display: inline-block; padding: 6px 10px; background: rgba(14,165,233,0.12); border: 1px solid rgba(14,165,233,0.35); color: #93c5fd; border-radius: 999px; font-size: 12px; margin-bottom: 12px; letter-spacing: .3px; }
        .hero h1 { font-size: clamp(28px, 5vw, 48px); line-height: 1.1; margin: 0 0 12px; }
        .hero p { color: var(--muted); font-size: 16px; max-width: 780px; margin: 0 auto 18px; }
        .gradient-text { background: linear-gradient(90deg, #60a5fa, #22d3ee 50%, #22c55e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .cta-buttons { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; animation: fadeInUp 1s ease 0.8s both; }
        .btn-primary { background: #fff; color: #000; border-radius: 10px; padding: 10px 14px; font-weight: 600; }
        .btn-secondary { border: 1px solid rgba(255,255,255,0.25); color: var(--fg); border-radius: 10px; padding: 10px 14px; font-weight: 600; }
        .features { padding: 48px 0; }
        .features-header { text-align: center; margin-bottom: 24px; }
        .features-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
        .feature-card { background: var(--card); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; transition: transform .15s ease; }
        .feature-card.in-view { transform: translateY(0); opacity: 1; }
        .feature-icon { width: 32px; height: 32px; display: grid; place-items: center; border-radius: 8px; background: rgba(14,165,233,0.12); border: 1px solid rgba(14,165,233,0.35); }
        .band { background: linear-gradient(90deg, rgba(14,165,233,.12), rgba(34,197,94,.12)); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; }
        .chips { display:flex; flex-wrap:wrap; gap:8px }
        .chip { border:1px solid rgba(255,255,255,.2); border-radius:999px; padding:4px 10px; font-size:12px }
        .stats { padding: 32px 0 56px; }
        .footer-bottom { margin-top: 16px; color: var(--muted); font-size: 12px; text-align: center; }
        @media (max-width: 900px) { .features-grid { grid-template-columns: 1fr; } }
        @keyframes fadeInUp{ from{opacity:0; transform: translate3d(0,10px,0)} to{opacity:1; transform: none} }
      `}</style>

      {/* Navbar */}
      <nav id="navbar" aria-label="Primary">
        <div className="container" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "12px 0" }}>
          <a href="/landing" className="logo" aria-label="Blackletter Systems">Blackletter Systems</a>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <a href="#how" className="btn-secondary">How it works</a>
            <a href="#faq" className="btn-secondary">FAQ</a>
            <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">Theme</button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero" id="home" aria-labelledby="hero-heading">
        <div className="container">
          <div className="hero-badge">{landing.tagline}</div>
          <h1 id="hero-heading">{landing.hero.h1}</h1>
          <p>{landing.hero.sub}</p>
          <div className="cta-buttons">
            {landing.hero.ctas.map((c) => (
              <a key={c.href} href={c.href} className={c.variant === "primary" ? "btn-primary" : "btn-secondary"} aria-label={c.label}>
                {c.label}
              </a>
            ))}
          </div>
          <p className="text-xs" aria-label="privacy note" style={{ marginTop: 8, color: "var(--muted)" }}>{landing.hero.micro}</p>
        </div>
      </section>

      {/* Value Props */}
      <section className="features" id="value" aria-labelledby="value-props-heading">
        <div className="features-header animate-on-scroll">
          <h2 id="value-props-heading">Why <span className="gradient-text">Blackletter</span></h2>
          <p style={{ color: "var(--muted)" }}>Compliance‑first, evidence‑first, UK‑centric.</p>
        </div>
        <div className="features-grid">
          {landing.valueProps.map((v, i) => (
            <div key={i} className="feature-card animate-on-scroll">
              <div className="feature-icon" aria-hidden />
              <h3 style={{ marginTop: 8 }}>{v.title}</h3>
              <p style={{ color: "var(--muted)", marginTop: 4 }}>{v.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="features" id="how" aria-labelledby="how-heading">
        <div className="features-header animate-on-scroll">
          <h2 id="how-heading">How it <span className="gradient-text">works</span></h2>
          <p style={{ color: "var(--muted)" }}>Four steps to explainable findings.</p>
        </div>
        <div className="features-grid">
          {landing.howItWorks.map((h, i) => (
            <div key={i} className="feature-card animate-on-scroll">
              <div className="feature-icon" aria-hidden />
              <h3 style={{ marginTop: 8 }}>{h.step}</h3>
              <p style={{ color: "var(--muted)", marginTop: 4 }}>{h.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Compliance Focus band */}
      <section className="container" aria-labelledby="compliance-heading" style={{ padding: "8px 0 24px" }}>
        <div className="band">
          <h2 id="compliance-heading" style={{ marginBottom: 8 }}>{landing.compliance.title}</h2>
          <div className="chips" style={{ marginBottom: 8 }}>
            {landing.compliance.items.map((t) => (
              <span key={t} className="chip">{t}</span>
            ))}
          </div>
          <div className="chips">
            {landing.compliance.targets.map((t) => (
              <span key={t} className="chip" style={{ borderColor: "rgba(34,197,94,.6)" }}>{t}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Pilot / CTA */}
      <section className="features" aria-labelledby="pilot-heading">
        <div className="features-header animate-on-scroll">
          <h2 id="pilot-heading">Pilot outcomes <span className="gradient-text">/ pricing</span></h2>
          <p style={{ color: "var(--muted)", marginBottom: 8 }}>{landing.pilot.pricing}</p>
          <p style={{ color: "var(--muted)", marginBottom: 12 }}>{landing.pilot.outcome}</p>
          <a href={landing.pilot.cta.href} className="btn-primary" aria-label={landing.pilot.cta.label}>{landing.pilot.cta.label}</a>
        </div>
      </section>

      {/* FAQ */}
      <section className="container" id="faq" aria-labelledby="faq-heading" style={{ paddingBottom: 40 }}>
        <h2 id="faq-heading" style={{ margin: "12px 0" }}>FAQ</h2>
        <div>
          {landing.faq.map((f, i) => (
            <details key={i} className="feature-card" style={{ marginBottom: 8 }}>
              <summary className="cursor-pointer" style={{ fontWeight: 600 }}>{f.q}</summary>
              <p style={{ color: "var(--muted)", marginTop: 8 }}>{f.a}</p>
            </details>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer aria-labelledby="footer-heading" style={{ borderTop: "1px solid rgba(255,255,255,0.08)" }}>
        <h2 id="footer-heading" className="visually-hidden">Footer</h2>
        <div className="footer-bottom">
          <p>© 2025 Blackletter Systems. {landing.footerNote}</p>
        </div>
      </footer>

      <style>{`.visually-hidden{position:absolute!important;height:1px;width:1px;overflow:hidden;clip:rect(1px,1px,1px,1px);white-space:nowrap;}`}</style>
    </>
  );
}
