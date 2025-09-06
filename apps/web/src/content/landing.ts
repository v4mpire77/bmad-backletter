export const landing = {
  tagline: "Old rules. New game.",
  hero: {
    h1: "The AI legal assistant built for UK compliance",
    sub: "Cut contract review time by 60% and never miss a GDPR obligation. Blackletter flags Article 28(3) clause gaps with explainable findings — snippet, rule ID, and rationale.",
    ctas: [
      {
        href: "/dashboard",
        label: "Try the Demo",
        variant: "primary",
      },
      {
        href: "/new",
        label: "Try the GDPR Checker",
        variant: "ghost",
      },
    ],
    micro: "Private by default. LLM is off unless you enable it. When enabled, we only send short snippets.",
  },
  valueProps: [
    { title: "Compliance‑first, not generic AI", body: "Purpose‑built for UK GDPR and SRA expectations — built to reduce risk, not just speed up text." },
    { title: "Explainable by design", body: "Every finding shows the clause snippet, detector rule ID, and short why so reviewers can validate quickly." },
    { title: "Auditable outputs", body: "Export a clean report (PDF/HTML) with findings, snippets, and timestamps — ready for internal sign‑off or vendor follow‑up." },
    { title: "Token‑disciplined, cost‑controlled", body: "LLM usage is optional and snippet‑only with hard caps. Deterministic rules do the heavy lifting." },
    { title: "Built for UK SMEs", body: "Designed for 10–200 fee‑earner firms. Windows‑friendly development with a simple path to scale." },
  ],
  howItWorks: [
      { step: "Upload", body: "Drop in a vendor DPA or lease (PDF/DOCX)." },
      { step: "Detect", body: "We run eight GDPR Article 28(3) checks using rulepacks + weak‑language patterns." },
      { step: "Review", body: "See Pass / Weak / Missing with snippet and rule ID. Filter by verdict." },
      { step: "Export", body: "Generate a shareable report for stakeholders." },
  ],
  compliance: {
      title: "Eight core checks, mapped to GDPR Article 28(3)",
      targets: ["p95 ≤ 60s / document", "Explainability ≥ 95%", "Cost ≈ £0.10 / document"],
      items: [
          "Instructions",
          "Confidentiality",
          "Security (Art.32)",
          "Sub‑processors & flow‑down",
          "Data‑subject rights assistance",
          "Breach notice",
          "Return/Delete",
          "Audits & information",
      ]
  },
  pilot: {
      pricing: "Early‑access pricing from £50–100 per user/month",
      outcome: "Target: 60% faster clause review with zero missed mandatory obligations in pilot cases.",
      cta: {
          href: "/dashboard",
          label: "Start a free demo",
      }
  },
  faq: [
      { q: "Is this a replacement for legal review?", a: "No. It’s a speed and consistency layer — evidence‑first findings to support professional judgement." },
      { q: "What data leaves the browser?", a: "Your file is processed server‑side. If you enable LLM, only short snippets are sent with token caps; otherwise processing stays rule‑first." },
      { q: "Which documents work best?", a: "Vendor DPAs, MSAs, and leases. PDF/DOCX up to 10MB." },
  ],
  footerNote: "Blackletter Systems provides software for compliance support. It does not provide legal advice. Results require professional review."
};
