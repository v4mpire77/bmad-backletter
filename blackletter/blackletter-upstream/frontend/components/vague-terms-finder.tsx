import React from 'react';
import { AlertTriangle, FileText, Clock, Shield, Zap } from 'lucide-react';

interface Citation {
  doc_id: string;
  page: number;
  start: number;
  end: number;
}

interface VagueTermFinding {
  issue: {
    id: string;
    title: string;
    description: string;
    severity: 'low' | 'medium' | 'high';
    clause: string;
    page_number: number;
    remediation: string;
  };
  vague_term: {
    text: string;
    category: string;
    severity: string;
    description: string;
    suggested_fix: string;
  };
  judgment: {
    verdict: 'non_compliant' | 'compliant' | 'weak';
    risk: 'low' | 'medium' | 'high';
    rationale: string;
    improvements: string[];
    quotes: Array<{
      text: string;
      citation: Citation;
    }>;
  };
  context: {
    context: string;
    page: number;
  };
  citations: Citation[];
}

interface VagueTermsFinderProps {
  findings: VagueTermFinding[];
  onCitationClick?: (citation: Citation) => void;
}

const getSeverityConfig = (severity: string) => {
  const configs = {
    low: {
      color: 'text-green-400 bg-green-500/10 border-green-500/30',
      icon: Shield,
      label: 'Low Risk'
    },
    medium: {
      color: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
      icon: AlertTriangle,
      label: 'Medium Risk'
    },
    high: {
      color: 'text-red-400 bg-red-500/10 border-red-500/30',
      icon: Zap,
      label: 'High Risk'
    }
  };
  return configs[severity as keyof typeof configs] || configs.medium;
};

export function VagueTermsFinder({ findings, onCitationClick }: VagueTermsFinderProps) {
  if (findings.length === 0) {
    return (
      <div className="text-center py-12">
        <Shield className="w-12 h-12 text-green-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-white mb-2">No Vague Terms Found</h3>
        <p className="text-gray-400">The contract appears to use clear, specific language.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Vague Terms Analysis</h2>
        <div className="flex items-center space-x-2 px-3 py-1 bg-amber-500/10 rounded-full border border-amber-500/20">
          <AlertTriangle className="w-4 h-4 text-amber-400" />
          <span className="text-xs text-amber-400 font-medium">
            {findings.length} VAGUE TERMS DETECTED
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {findings.map((finding, index) => {
          const severityConfig = getSeverityConfig(finding.judgment.risk);
          const Icon = severityConfig.icon;

          return (
            <div
              key={finding.issue.id}
              className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50 hover:border-gray-700/50 transition-all"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg border ${severityConfig.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white">{finding.issue.title}</h3>
                    <p className="text-sm text-gray-400">{finding.vague_term.category}</p>
                  </div>
                </div>
                <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium border ${severityConfig.color}`}>
                  <span>{severityConfig.label}</span>
                </div>
              </div>

              <div className="mb-4">
                <div className="bg-gray-800/30 rounded-lg p-4 mb-3">
                  <div className="text-sm text-gray-400 mb-2">Flagged Term:</div>
                  <div className="font-mono text-amber-400 bg-amber-500/10 px-2 py-1 rounded">
                    "{finding.vague_term.text}"
                  </div>
                </div>

                <div className="text-sm text-gray-300 mb-3">
                  <strong>Why this is problematic:</strong> {finding.judgment.rationale}
                </div>

                {finding.judgment.improvements.length > 0 && (
                  <div className="mb-3">
                    <div className="text-sm text-gray-400 mb-2">Suggested Fix:</div>
                    <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3">
                      <div className="text-sm text-green-300">
                        {finding.judgment.improvements[0]}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-4 text-gray-500">
                  <span className="flex items-center space-x-1">
                    <FileText className="w-3 h-3" />
                    <span>Page {finding.context.page}</span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <Clock className="w-3 h-3" />
                    <span>{finding.vague_term.severity} severity</span>
                  </span>
                </div>

                {finding.citations.length > 0 && (
                  <button
                    onClick={() => onCitationClick?.(finding.citations[0])}
                    className="text-blue-400 hover:text-blue-300 text-sm font-medium"
                  >
                    View in Document →
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
