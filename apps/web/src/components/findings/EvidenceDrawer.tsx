import type { Finding } from "@/hooks/useFindings";

export default function EvidenceDrawer({ finding, onClose }: { finding: Finding | null; onClose: () => void }) {
  return (
    <div className={`fixed inset-0 z-50 ${finding ? "pointer-events-auto" : "pointer-events-none"}`}>
      <div className={`absolute inset-0 bg-black/30 ${finding ? "opacity-100" : "opacity-0"}`} onClick={onClose} />
      <aside
        className={`absolute right-0 top-0 h-full w-full max-w-xl bg-white shadow-xl p-4 transition-transform ${
          finding ? "translate-x-0" : "translate-x-full"
        }`}
        aria-hidden={!finding}
      >
        {finding && (
          <div className="space-y-3">
            <h2 className="text-lg font-semibold">
              {finding.rule_id} <span className="text-gray-500 text-sm">(p.{finding.page})</span>
            </h2>
            <p className="text-sm text-gray-800 whitespace-pre-wrap">{finding.snippet}</p>
            {finding.rationale && <p className="text-xs text-gray-500">Rationale: {finding.rationale}</p>}
            <div className="flex justify-end pt-2">
              <button className="text-sm underline" onClick={onClose}>
                Close
              </button>
            </div>
          </div>
        )}
      </aside>
    </div>
  );
}

