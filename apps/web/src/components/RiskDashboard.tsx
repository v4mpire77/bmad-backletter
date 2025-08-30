"use client";

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';

interface RiskFactor {
  category: string;
  level: string;
  score: number;
  description: string;
  evidence: string;
  recommendations: string[];
  impact: string;
}

interface RiskProfile {
  overall_score: number;
  overall_level: string;
  risk_factors: RiskFactor[];
  summary: string;
  urgent_actions: string[];
  monitoring_points: string[];
}

interface RiskAnalysisResponse {
  analysis_id: string;
  risk_profile: RiskProfile;
  metadata: any;
}

interface WebSocketMessage {
  type: string;
  analysis_id: string;
  data?: any;
  message?: string;
}

export default function RiskDashboard({ analysisId }: { analysisId: string }) {
  const [riskProfile, setRiskProfile] = useState<RiskProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [liveUpdates, setLiveUpdates] = useState<WebSocketMessage[]>([]);
  
  const wsRef = useRef<WebSocket | null>(null);
  const router = useRouter();

  // Fetch initial risk analysis
  useEffect(() => {
    fetchRiskAnalysis();
  }, [analysisId]);

  // WebSocket connection for real-time updates
  useEffect(() => {
    if (!analysisId) return;

    const wsUrl = `${process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'}/ws/analysis/${analysisId}`;
    const ws = new WebSocket(wsUrl.replace('http', 'ws'));

    ws.onopen = () => {
      setWsConnected(true);
      console.log('WebSocket connected for real-time risk updates');
    };

    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        setLiveUpdates(prev => [...prev, message]);
        
        // Handle different message types
        if (message.type === 'risk_update') {
          // Refresh risk analysis on updates
          fetchRiskAnalysis();
        }
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };

    ws.onclose = () => {
      setWsConnected(false);
      console.log('WebSocket disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsConnected(false);
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [analysisId]);

  const fetchRiskAnalysis = async () => {
    try {
      setLoading(true);
      const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
      const response = await fetch(`${base}/api/risk-analysis/${analysisId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: RiskAnalysisResponse = await response.json();
      setRiskProfile(data.risk_profile);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch risk analysis');
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical': return 'bg-red-600 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-black';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getRiskLevelIcon = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical': return '🚨';
      case 'high': return '⚠️';
      case 'medium': return '⚡';
      case 'low': return '✅';
      default: return 'ℹ️';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'compliance': return '🛡️';
      case 'financial': return '💰';
      case 'operational': return '⚙️';
      case 'reputational': return '🏢';
      case 'legal': return '⚖️';
      default: return '📋';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-lg">Analyzing contract risk...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <div className="text-red-600 text-xl mb-2">⚠️ Risk Analysis Failed</div>
        <div className="text-red-700 mb-4">{error}</div>
        <button 
          onClick={fetchRiskAnalysis}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Retry Analysis
        </button>
      </div>
    );
  }

  if (!riskProfile) {
    return (
      <div className="text-center p-8 text-gray-500">
        No risk profile available for this analysis.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Connection Status */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="text-sm text-gray-600">
            {wsConnected ? 'Live updates connected' : 'Live updates disconnected'}
          </span>
        </div>
        <button
          onClick={fetchRiskAnalysis}
          className="text-sm text-blue-600 hover:text-blue-800 underline"
        >
          Refresh Analysis
        </button>
      </div>

      {/* Overall Risk Summary */}
      <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-blue-500">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Contract Risk Profile</h2>
          <div className={`px-4 py-2 rounded-full text-sm font-semibold ${getRiskLevelColor(riskProfile.overall_level)}`}>
            {getRiskLevelIcon(riskProfile.overall_level)} {riskProfile.overall_level.toUpperCase()}
          </div>
        </div>
        
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Overall Risk Score</span>
            <span className="text-sm text-gray-500">{Math.round(riskProfile.overall_score * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all duration-500 ${
                riskProfile.overall_score >= 0.8 ? 'bg-red-600' :
                riskProfile.overall_score >= 0.6 ? 'bg-orange-500' :
                riskProfile.overall_score >= 0.4 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${riskProfile.overall_score * 100}%` }}
            ></div>
          </div>
        </div>

        <p className="text-gray-700 leading-relaxed">{riskProfile.summary}</p>
      </div>

      {/* Urgent Actions */}
      {riskProfile.urgent_actions.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-red-800 mb-3 flex items-center">
            🚨 Urgent Actions Required
          </h3>
          <ul className="space-y-2">
            {riskProfile.urgent_actions.map((action, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-red-600 mt-1">•</span>
                <span className="text-red-700">{action}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Risk Factors Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {riskProfile.risk_factors.map((factor, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <span className="text-2xl">{getCategoryIcon(factor.category)}</span>
                <h4 className="font-semibold text-gray-900 capitalize">{factor.category}</h4>
              </div>
              <div className={`px-3 py-1 rounded-full text-xs font-semibold ${getRiskLevelColor(factor.level)}`}>
                {getRiskLevelIcon(factor.level)} {factor.level}
              </div>
            </div>

            <div className="mb-3">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-gray-600">Risk Score</span>
                <span className="text-xs text-gray-500">{Math.round(factor.score * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div 
                  className={`h-1.5 rounded-full ${
                    factor.score >= 0.8 ? 'bg-red-600' :
                    factor.score >= 0.6 ? 'bg-orange-500' :
                    factor.score >= 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                  }`}
                  style={{ width: `${factor.score * 100}%` }}
                ></div>
              </div>
            </div>

            <p className="text-sm text-gray-700 mb-3">{factor.description}</p>
            
            <div className="mb-3">
              <span className="text-xs font-medium text-gray-600">Evidence:</span>
              <p className="text-xs text-gray-600 mt-1">{factor.evidence}</p>
            </div>

            <div className="mb-3">
              <span className="text-xs font-medium text-gray-600">Impact:</span>
              <span className={`ml-2 px-2 py-1 rounded text-xs font-medium ${
                factor.impact.toLowerCase() === 'high' ? 'bg-red-100 text-red-800' :
                factor.impact.toLowerCase() === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {factor.impact}
              </span>
            </div>

            {factor.recommendations.length > 0 && (
              <div>
                <span className="text-xs font-medium text-gray-600">Recommendations:</span>
                <ul className="mt-1 space-y-1">
                  {factor.recommendations.slice(0, 2).map((rec, recIndex) => (
                    <li key={recIndex} className="text-xs text-gray-600 flex items-start space-x-1">
                      <span className="text-blue-600 mt-0.5">→</span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Monitoring Points */}
      {riskProfile.monitoring_points.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-3 flex items-center">
            📊 Monitoring Points
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {riskProfile.monitoring_points.map((point, index) => (
              <div key={index} className="flex items-center space-x-2">
                <span className="text-blue-600">•</span>
                <span className="text-blue-700 text-sm">{point}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Live Updates */}
      {liveUpdates.length > 0 && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            🔴 Live Updates
          </h3>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {liveUpdates.slice(-5).map((update, index) => (
              <div key={index} className="text-sm text-gray-600 bg-white p-2 rounded border">
                <span className="font-medium">{update.type}:</span> {update.message || update.data}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
