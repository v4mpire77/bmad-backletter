<<<<<<< HEAD
/**
 * Blackletter GDPR Processor - Dashboard Page
 * Context Engineering Framework v2.0.0 Compliant
 * Real-time job monitoring and results visualization
 */
"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { BlackletterAPIClient, BlackletterAPIError } from "@/lib/api";
import { 
  JobStatus, 
  JobResult, 
  JobStatusEnum, 
  JobWithDetails, 
  Issue, 
  Coverage,
  GDPR_ARTICLES
} from "@/lib/types";

// Initialize API client
const apiClient = new BlackletterAPIClient();

const POLL_INTERVAL = 5000; // 5 seconds
const MAX_RETRIES = 3;

export default function DashboardPage() {
  const [jobs, setJobs] = useState<JobWithDetails[]>([]);
  const [selectedJob, setSelectedJob] = useState<string | null>(null);
  const [jobResult, setJobResult] = useState<JobResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  // Fetch jobs from API
  const fetchJobs = useCallback(async () => {
    try {
      const jobsList = await apiClient.listJobs(50);
      setJobs(jobsList as JobWithDetails[]);
      setError(null);
      setRetryCount(0);
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
      if (err instanceof BlackletterAPIError) {
        setError(`API Error: ${err.message} (${err.statusCode})`);
      } else {
        setError('Failed to fetch jobs. Please check your connection.');
      }
      
      // Retry logic
      if (retryCount < MAX_RETRIES) {
        setRetryCount(prev => prev + 1);
        setTimeout(fetchJobs, 1000 * (retryCount + 1)); // Exponential backoff
      }
    } finally {
      setLoading(false);
    }
  }, [retryCount]);

  // Fetch job result
  const fetchJobResult = useCallback(async (jobId: string) => {
    try {
      const result = await apiClient.getJobResult(jobId);
      setJobResult(result);
    } catch (err) {
      console.error(`Failed to fetch result for job ${jobId}:`, err);
      // Don't show error for 202 responses (still processing)
      if (err instanceof BlackletterAPIError && err.statusCode !== 202) {
        setError(`Failed to fetch job result: ${err.message}`);
      }
    }
  }, []);

  // Cancel job
  const handleCancelJob = async (jobId: string) => {
    try {
      await apiClient.cancelJob(jobId);
      fetchJobs(); // Refresh jobs list
    } catch (err) {
      console.error(`Failed to cancel job ${jobId}:`, err);
      if (err instanceof BlackletterAPIError) {
        setError(`Failed to cancel job: ${err.message}`);
      }
    }
  };

  // Initial load and polling
  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchJobs]);

  // Fetch result when job is selected
  useEffect(() => {
    if (selectedJob) {
      const job = jobs.find(j => j.job_id === selectedJob);
      if (job && job.status === 'completed') {
        fetchJobResult(selectedJob);
      } else {
        setJobResult(null);
      }
    }
  }, [selectedJob, jobs, fetchJobResult]);

  const getStatusColor = (status: JobStatusEnum): string => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'failed': return 'bg-red-500';
      case 'processing': return 'bg-yellow-500';
      case 'cancelled': return 'bg-gray-500';
      default: return 'bg-blue-500';
    }
  };

  const getStatusText = (status: JobStatusEnum): string => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  const getCoverageColor = (status: string): string => {
    switch (status) {
      case 'OK': return 'text-green-600 bg-green-50';
      case 'Partial': return 'text-yellow-600 bg-yellow-50';
      case 'GAP': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getSeverityColor = (severity: string): string => {
    switch (severity) {
      case 'High': return 'text-red-600 bg-red-50';
      case 'Medium': return 'text-yellow-600 bg-yellow-50';
      case 'Low': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  if (loading && jobs.length === 0) {
    return (
      <div className="container mx-auto py-10 px-4">
        <div className="space-y-6">
          <Skeleton className="h-8 w-64" />
          <div className="grid gap-4">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-24 w-full" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10 px-4">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Contract Analysis Dashboard</h1>
            <p className="text-muted-foreground">
              Monitor GDPR Article 28(3) processor obligations analysis
            </p>
          </div>
          <Button onClick={fetchJobs} variant="outline">
            Refresh
          </Button>
        </div>

        {/* Error Display */}
        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600">{error}</p>
              <Button onClick={fetchJobs} className="mt-2" variant="outline" size="sm">
                Retry
              </Button>
            </CardContent>
          </Card>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Jobs List */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Jobs ({jobs.length})</CardTitle>
              <CardDescription>
                Analysis jobs with real-time status updates
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {jobs.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <p>No jobs found.</p>
                  <p className="text-sm">Upload a contract to get started!</p>
                </div>
              ) : (
                jobs.map((job) => (
                  <div
                    key={job.job_id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      selectedJob === job.job_id 
                        ? 'border-primary bg-primary/5' 
                        : 'border-border hover:border-primary/50'
                    }`}
                    onClick={() => setSelectedJob(job.job_id)}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">
                          {job.filename || `Job ${job.job_id.slice(0, 8)}`}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {new Date(job.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={getStatusColor(job.status)}>
                          {getStatusText(job.status)}
                        </Badge>
                        {(job.status === 'pending' || job.status === 'processing') && (
                          <Button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCancelJob(job.job_id);
                            }}
                            variant="outline"
                            size="sm"
                          >
                            Cancel
                          </Button>
                        )}
                      </div>
                    </div>

                    {/* Progress Bar */}
                    {job.status === 'processing' && (
                      <div className="space-y-1">
                        <Progress value={job.progress * 100} className="h-2" />
                        <p className="text-xs text-muted-foreground">
                          {Math.round(job.progress * 100)}% complete
                        </p>
                      </div>
                    )}

                    {/* Status Message */}
                    {job.message && (
                      <p className="text-sm text-muted-foreground mt-2">
                        {job.message}
                      </p>
                    )}
                  </div>
                ))
              )}
            </CardContent>
          </Card>

          {/* Job Results */}
          <Card>
            <CardHeader>
              <CardTitle>Analysis Results</CardTitle>
              <CardDescription>
                {selectedJob 
                  ? `Results for job ${selectedJob.slice(0, 8)}...`
                  : 'Select a completed job to view results'
                }
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!selectedJob ? (
                <div className="text-center py-8 text-muted-foreground">
                  Select a job from the list to view detailed results
                </div>
              ) : !jobResult ? (
                <div className="space-y-4">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                </div>
              ) : jobResult.error ? (
                <div className="text-center py-8">
                  <p className="text-red-600 font-medium">Analysis Failed</p>
                  <p className="text-sm text-muted-foreground mt-2">
                    {jobResult.error}
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Summary */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-blue-50 rounded-lg">
                      <p className="text-2xl font-bold text-blue-600">
                        {jobResult.analysis?.issues.length || 0}
                      </p>
                      <p className="text-sm text-blue-600">Issues Found</p>
                    </div>
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                      <p className="text-2xl font-bold text-green-600">
                        {jobResult.analysis?.coverage.filter(c => c.status === 'OK').length || 0}/8
                      </p>
                      <p className="text-sm text-green-600">Articles OK</p>
                    </div>
                  </div>

                  {/* GDPR Coverage */}
                  {jobResult.analysis?.coverage && (
                    <div>
                      <h4 className="font-medium mb-3">GDPR Article 28(3) Coverage</h4>
                      <div className="space-y-2">
                        {GDPR_ARTICLES.map((article) => {
                          const coverage = jobResult.analysis?.coverage.find(
                            c => c.article === article.article
                          );
                          const status = coverage?.status || 'GAP';
                          
                          return (
                            <div key={article.article} className="flex justify-between items-center p-2 border rounded">
                              <div>
                                <p className="font-medium text-sm">{article.article}</p>
                                <p className="text-xs text-muted-foreground">{article.name}</p>
                              </div>
                              <Badge className={getCoverageColor(status)}>
                                {status}
                              </Badge>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Issues */}
                  {jobResult.analysis?.issues && jobResult.analysis.issues.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-3">Issues Detected</h4>
                      <div className="space-y-3 max-h-64 overflow-y-auto">
                        {jobResult.analysis.issues.map((issue) => (
                          <div key={issue.id} className="p-3 border rounded-lg">
                            <div className="flex justify-between items-start mb-2">
                              <p className="font-medium text-sm">{issue.citation}</p>
                              <Badge className={getSeverityColor(issue.severity)}>
                                {issue.severity}
                              </Badge>
                            </div>
                            <p className="text-sm text-muted-foreground mb-2">
                              {issue.snippet}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              Confidence: {Math.round(issue.confidence * 100)}%
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Processing Time */}
                  {jobResult.processing_time && (
                    <div className="text-xs text-muted-foreground text-center pt-4 border-t">
                      Processed in {jobResult.processing_time.toFixed(2)} seconds
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
=======
"use client";

import React, { useState, useEffect, useMemo } from "react";
import { 
  Upload, FileText, AlertTriangle, Scale, ShieldCheck, 
  Gavel, Filter, Search, Download, RefreshCw, Sparkles,
  Sun, Moon
} from "lucide-react";

// Temporarily commenting out problematic imports to fix build
// TODO: Fix UI component resolution in build process
/*
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
*/

// Temporary fallback components
const Button = ({ children, className, ...props }: any) => (
  <button className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 ${className}`} {...props}>
    {children}
  </button>
);

const Card = ({ children, className, ...props }: any) => (
  <div className={`border rounded-lg shadow ${className}`} {...props}>
    {children}
  </div>
);

const CardHeader = ({ children, className, ...props }: any) => (
  <div className={`border-b p-4 ${className}`} {...props}>
    {children}
  </div>
);

const CardTitle = ({ children, className, ...props }: any) => (
  <h3 className={`text-lg font-semibold ${className}`} {...props}>
    {children}
  </h3>
);

const CardContent = ({ children, className, ...props }: any) => (
  <div className={`p-4 ${className}`} {...props}>
    {children}
  </div>
);

const Input = ({ className, ...props }: any) => (
  <input className={`border rounded px-3 py-2 ${className}`} {...props} />
);

const Label = ({ children, className, ...props }: any) => (
  <label className={`block text-sm font-medium ${className}`} {...props}>
    {children}
  </label>
);

const Select = ({ children, className, ...props }: any) => (
  <select className={`border rounded px-3 py-2 ${className}`} {...props}>
    {children}
  </select>
);

const SelectContent = ({ children }: any) => <>{children}</>;
const SelectItem = ({ children, value, ...props }: any) => (
  <option value={value} {...props}>{children}</option>
);
const SelectTrigger = ({ children }: any) => <>{children}</>;
const SelectValue = () => null;

// Additional temporary fallback components
const Switch = ({ checked, onCheckedChange, className, ...props }: any) => (
  <input 
    type="checkbox" 
    checked={checked} 
    onChange={(e) => onCheckedChange?.(e.target.checked)}
    className={`rounded ${className}`} 
    {...props} 
  />
);

const Badge = ({ children, className, ...props }: any) => (
  <span className={`inline-block px-2 py-1 text-xs rounded ${className}`} {...props}>
    {children}
  </span>
);

const Table = ({ children, className, ...props }: any) => (
  <table className={`w-full border-collapse ${className}`} {...props}>
    {children}
  </table>
);
const TableBody = ({ children, ...props }: any) => <tbody {...props}>{children}</tbody>;
const TableCell = ({ children, className, ...props }: any) => (
  <td className={`border px-4 py-2 ${className}`} {...props}>{children}</td>
);
const TableHead = ({ children, className, ...props }: any) => (
  <th className={`border px-4 py-2 font-semibold ${className}`} {...props}>{children}</th>
);
const TableHeader = ({ children, ...props }: any) => <thead {...props}>{children}</thead>;
const TableRow = ({ children, className, ...props }: any) => (
  <tr className={`border-b ${className}`} {...props}>{children}</tr>
);

const Textarea = ({ className, ...props }: any) => (
  <textarea className={`border rounded px-3 py-2 ${className}`} {...props} />
);

const Dialog = ({ children, ...props }: any) => <div {...props}>{children}</div>;
const DialogContent = ({ children, className, ...props }: any) => (
  <div className={`fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 ${className}`} {...props}>
    <div className="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
      {children}
    </div>
  </div>
);
const DialogHeader = ({ children, ...props }: any) => <div {...props}>{children}</div>;
const DialogTitle = ({ children, className, ...props }: any) => (
  <h2 className={`text-xl font-semibold ${className}`} {...props}>{children}</h2>
);
const DialogTrigger = ({ children, ...props }: any) => <div {...props}>{children}</div>;

const Tabs = ({ children, ...props }: any) => <div {...props}>{children}</div>;
const TabsContent = ({ children, className, ...props }: any) => (
  <div className={`mt-4 ${className}`} {...props}>{children}</div>
);
const TabsList = ({ children, className, ...props }: any) => (
  <div className={`flex border-b ${className}`} {...props}>{children}</div>
);
const TabsTrigger = ({ children, className, ...props }: any) => (
  <button className={`px-4 py-2 border-b-2 ${className}`} {...props}>{children}</button>
);

const Separator = ({ className, ...props }: any) => (
  <hr className={`border-gray-300 ${className}`} {...props} />
);

// Recharts imports
import {
  BarChart as RBarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip as RTooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  ResponsiveContainer,
} from "recharts";

// Types
interface Issue {
  id: string;
  docId: string;
  docName: string;
  type: "GDPR" | "Statute" | "Case Law";
  severity: "High" | "Medium" | "Low";
  status: "Open" | "In Review" | "Resolved";
  confidence: number;
  snippet: string;
  recommendation: string;
  clausePath: string;
  citation: string;
  createdAt: string;
}

// Mock data
const mockIssues: Issue[] = [
  {
    id: "ISS-001",
    docId: "DOC-001",
    docName: "Service Agreement v2.1.pdf",
    type: "GDPR",
    severity: "High",
    status: "Open",
    confidence: 0.92,
    snippet: "Personal data may be transferred to third countries without adequate protection...",
    recommendation: "Add explicit GDPR compliance clauses and ensure adequate data protection measures",
    clausePath: "Section 8.2 - Data Processing",
    citation: "UK GDPR Article 44",
    createdAt: "2025-08-14T10:22:00Z"
  },
  {
    id: "ISS-002", 
    docId: "DOC-001",
    docName: "Service Agreement v2.1.pdf",
    type: "Statute",
    severity: "Medium",
    status: "In Review",
    confidence: 0.87,
    snippet: "Limitation of liability clause may not comply with UK consumer protection laws...",
    recommendation: "Review and revise liability limitations to ensure compliance with Consumer Rights Act 2015",
    clausePath: "Section 12 - Limitation of Liability",
    citation: "Consumer Rights Act 2015, Section 62",
    createdAt: "2025-08-14T11:15:00Z"
  },
  {
    id: "ISS-003",
    docId: "DOC-002", 
    docName: "Privacy Policy v1.3.pdf",
    type: "Case Law",
    severity: "Low",
    status: "Resolved",
    confidence: 0.76,
    snippet: "Cookie consent mechanism could be strengthened based on recent ICO guidance...",
    recommendation: "Implement more granular cookie consent options following Planet49 case precedent",
    clausePath: "Section 4 - Cookie Policy",
    citation: "Planet49 GmbH v Bundesverband (C-673/17)",
    createdAt: "2025-08-14T14:30:00Z"
  }
];

const mockDocs = [
  { id: "DOC-001", name: "Service Agreement v2.1.pdf", uploadedAt: "2 days ago" },
  { id: "DOC-002", name: "Privacy Policy v1.3.pdf", uploadedAt: "1 week ago" },
  { id: "DOC-003", name: "Terms of Use v4.0.pdf", uploadedAt: "3 days ago" }
];

export default function Dashboard() {
  // State
  const [darkMode, setDarkMode] = useState(false);
  const [apiHealth, setApiHealth] = useState<'loading' | 'ok' | 'error'>('loading');
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState<"All" | "GDPR" | "Statute" | "Case Law">("All");
  const [severityFilter, setSeverityFilter] = useState<"All" | "High" | "Medium" | "Low">("All");
  const [statusFilter, setStatusFilter] = useState<"All" | "Open" | "In Review" | "Resolved">("All");
  const [gdprFocus, setGdprFocus] = useState(false);
  const [hideResolved, setHideResolved] = useState(false);
  const [issues, setIssues] = useState<Issue[]>(mockIssues);

  // Check API health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
          setApiHealth('ok');
        } else {
          setApiHealth('error');
        }
      } catch (error) {
        setApiHealth('error');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Filter issues
  const filteredIssues = useMemo(() => {
    return issues.filter((issue) => {
      const matchesSearch = issue.snippet.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           issue.docName.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = typeFilter === "All" || issue.type === typeFilter;
      const matchesSeverity = severityFilter === "All" || issue.severity === severityFilter;
      const matchesStatus = statusFilter === "All" || issue.status === statusFilter;
      const matchesGdpr = !gdprFocus || issue.type === "GDPR";
      const matchesResolved = !hideResolved || issue.status !== "Resolved";
      
      return matchesSearch && matchesType && matchesSeverity && matchesStatus && matchesGdpr && matchesResolved;
    });
  }, [issues, searchTerm, typeFilter, severityFilter, statusFilter, gdprFocus, hideResolved]);

  // Calculate KPIs
  const kpis = useMemo(() => {
    const uniqueDocs = new Set(filteredIssues.map(i => i.docId)).size;
    const avgConfidence = filteredIssues.length > 0
      ? filteredIssues.reduce((sum, i) => sum + i.confidence, 0) / filteredIssues.length
      : 0;
    
    return {
      totalDocs: uniqueDocs,
      high: filteredIssues.filter(i => i.severity === "High").length,
      medium: filteredIssues.filter(i => i.severity === "Medium").length,
      low: filteredIssues.filter(i => i.severity === "Low").length,
      avgConfidence
    };
  }, [filteredIssues]);

  // Chart data
  const distByType = [
    { name: "GDPR", value: filteredIssues.filter(i => i.type === "GDPR").length },
    { name: "Statute", value: filteredIssues.filter(i => i.type === "Statute").length },
    { name: "Case Law", value: filteredIssues.filter(i => i.type === "Case Law").length },
  ];

  const distBySeverity = [
    { name: "High", value: kpis.high, color: "#ef4444" },
    { name: "Medium", value: kpis.medium, color: "#f59e0b" },
    { name: "Low", value: kpis.low, color: "#10b981" },
  ];

  // Helper function
  const toPercent = (decimal: number) => (decimal * 100).toFixed(1) + '%';

  return (
    <div className={darkMode ? 'min-h-screen dark bg-gray-900' : 'min-h-screen bg-gray-50'}>
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              Contract Review Dashboard
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              UK Law Compliance Analysis
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* API Status */}
            <div className={apiHealth === 'ok' ? 'px-2 py-1 rounded-full text-xs flex items-center gap-1.5 bg-green-500/10 text-green-400 border border-green-500/20' : apiHealth === 'error' ? 'px-2 py-1 rounded-full text-xs flex items-center gap-1.5 bg-red-500/10 text-red-400 border border-red-500/20' : 'px-2 py-1 rounded-full text-xs flex items-center gap-1.5 bg-gray-700 text-gray-400 border border-gray-600'}>
              <div className={apiHealth === 'ok' ? 'w-1.5 h-1.5 rounded-full bg-green-400' : apiHealth === 'error' ? 'w-1.5 h-1.5 rounded-full bg-red-400' : 'w-1.5 h-1.5 rounded-full bg-gray-400'} />
              {apiHealth === 'loading' ? 'Connecting...' : apiHealth.toUpperCase()}
            </div>

            {/* Dark Mode Toggle */}
            <Button
              variant="outline"
              size="sm"
              onClick={() => setDarkMode(!darkMode)}
              className="flex items-center gap-2"
            >
              {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              {darkMode ? "Light" : "Dark"}
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex flex-col lg:flex-row gap-6 max-w-7xl mx-auto">
          {/* Sidebar Filters */}
          <div className="w-full lg:w-80 lg:shrink-0">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Filter className="h-4 w-4" /> Filters
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>Issue Type</Label>
                  <Select value={typeFilter} onValueChange={(v) => setTypeFilter(v as any)}>
                    <SelectTrigger>
                      <SelectValue placeholder="All" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="All">All</SelectItem>
                      <SelectItem value="GDPR">GDPR</SelectItem>
                      <SelectItem value="Statute">Statute</SelectItem>
                      <SelectItem value="Case Law">Case Law</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Severity</Label>
                  <Select value={severityFilter} onValueChange={(v) => setSeverityFilter(v as any)}>
                    <SelectTrigger>
                      <SelectValue placeholder="All" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="All">All</SelectItem>
                      <SelectItem value="High">High</SelectItem>
                      <SelectItem value="Medium">Medium</SelectItem>
                      <SelectItem value="Low">Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Status</Label>
                  <Select value={statusFilter} onValueChange={(v) => setStatusFilter(v as any)}>
                    <SelectTrigger>
                      <SelectValue placeholder="All" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="All">All</SelectItem>
                      <SelectItem value="Open">Open</SelectItem>
                      <SelectItem value="In Review">In Review</SelectItem>
                      <SelectItem value="Resolved">Resolved</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <Separator />

                <div className="space-y-2">
                  <Label>Search</Label>
                  <div className="relative">
                    <Search className="absolute left-2 top-2.5 h-4 w-4 text-gray-400" />
                    <Input
                      placeholder="Search issues..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-8"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <Label htmlFor="gdpr-focus">GDPR Focus</Label>
                  <Switch 
                    id="gdpr-focus"
                    checked={gdprFocus}
                    onCheckedChange={setGdprFocus}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <Label htmlFor="hide-resolved">Hide Resolved</Label>
                  <Switch
                    id="hide-resolved"
                    checked={hideResolved}
                    onCheckedChange={setHideResolved}
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content Area */}
          <div className="flex-1 space-y-6">
            {/* KPIs */}
            <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Documents Scanned</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{kpis.totalDocs}</CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">High Risk</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{kpis.high}</CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Med / Low</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{kpis.medium} / {kpis.low}</CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Model Confidence</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{toPercent(kpis.avgConfidence)}</CardContent>
              </Card>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <Card>
                <CardHeader className="pb-0">
                  <CardTitle className="flex items-center gap-2 text-base">
                    <Gavel className="h-4 w-4" /> Issues by Type
                  </CardTitle>
                </CardHeader>
                <CardContent className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <RBarChart data={distByType}>
                      <XAxis dataKey="name" />
                      <YAxis allowDecimals={false} />
                      <RTooltip />
                      <Legend />
                      <Bar dataKey="value" name="Count" fill="#3b82f6" />
                    </RBarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-0">
                  <CardTitle className="flex items-center gap-2 text-base">
                    <Scale className="h-4 w-4" /> Issues by Severity
                  </CardTitle>
                </CardHeader>
                <CardContent className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie 
                        data={distBySeverity} 
                        dataKey="value" 
                        nameKey="name" 
                        outerRadius={80} 
                        label 
                      >
                        {distBySeverity.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Legend />
                      <RTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Issues Table */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Gavel className="h-4 w-4" /> Open Issues
                </CardTitle>
                <div className="text-sm text-neutral-500 dark:text-neutral-400">
                  Showing {filteredIssues.length} of {issues.length} issues
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Document</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Severity</TableHead>
                      <TableHead>Snippet</TableHead>
                      <TableHead>Confidence</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredIssues.map((issue) => (
                      <TableRow key={issue.id}>
                        <TableCell>
                          <div className="max-w-[150px] truncate">{issue.docName}</div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">{issue.type}</Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={issue.severity === "High" ? "destructive" : issue.severity === "Medium" ? "secondary" : "default"}>
                            {issue.severity}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="max-w-[250px] truncate text-sm">{issue.snippet}</div>
                        </TableCell>
                        <TableCell>{toPercent(issue.confidence)}</TableCell>
                        <TableCell>
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="outline" size="sm">View</Button>
                            </DialogTrigger>
                            <DialogContent className="max-w-4xl">
                              <DialogHeader>
                                <DialogTitle>{issue.id} - {issue.docName}</DialogTitle>
                              </DialogHeader>
                              <Tabs defaultValue="details" className="w-full">
                                <TabsList>
                                  <TabsTrigger value="details">Details</TabsTrigger>
                                  <TabsTrigger value="trace">LLM Trace</TabsTrigger>
                                  <TabsTrigger value="citations">Citations</TabsTrigger>
                                  <TabsTrigger value="history">History</TabsTrigger>
                                </TabsList>

                                <TabsContent value="details" className="space-y-4">
                                  <div className="grid grid-cols-2 gap-4">
                                    <div>
                                      <Label>Clause Path</Label>
                                      <p className="mt-1">{issue.clausePath}</p>
                                    </div>
                                    <div>
                                      <Label>Citation</Label>
                                      <p className="mt-1">{issue.citation}</p>
                                    </div>
                                  </div>

                                  <div>
                                    <Label>Snippet</Label>
                                    <Textarea value={issue.snippet} readOnly className="mt-1" rows={3} />
                                  </div>

                                  <div>
                                    <Label>Recommendation</Label>
                                    <Textarea value={issue.recommendation} readOnly className="mt-1" rows={4} />
                                  </div>
                                </TabsContent>

                                <TabsContent value="trace" className="space-y-4">
                                  <div className="rounded bg-neutral-50 p-4 dark:bg-neutral-800">
                                    <pre className="whitespace-pre-wrap text-sm">
{`Model: gpt-4-turbo
Input Tokens: 2,847
Output Tokens: 312
Latency: 2.3s

System: You are a UK legal compliance expert...
User: Analyze this clause for GDPR compliance...
Assistant: I've identified a high-severity GDPR issue...`}
                                    </pre>
                                  </div>
                                </TabsContent>

                                <TabsContent value="citations" className="space-y-4">
                                  <div className="space-y-2">
                                    <div className="rounded border p-3">
                                      <div className="font-medium">UK GDPR Article 44</div>
                                      <div className="mt-1 text-neutral-600 dark:text-neutral-400">
                                        General principle for transfers: Any transfer of personal data...
                                      </div>
                                    </div>
                                    <div className="rounded border p-3">
                                      <div className="font-medium">DPA 2018 Part 2</div>
                                      <div className="mt-1 text-neutral-600 dark:text-neutral-400">
                                        Processing for law enforcement purposes...
                                      </div>
                                    </div>
                                  </div>
                                </TabsContent>

                                <TabsContent value="history" className="space-y-4">
                                  <div className="space-y-2">
                                    <div className="flex items-center gap-2 text-sm">
                                      <span className="text-neutral-500">2025-08-14 10:22</span>
                                      <span>Created by AI Analysis</span>
                                    </div>
                                    <div className="flex items-center gap-2 text-sm">
                                      <span className="text-neutral-500">2025-08-14 15:30</span>
                                      <span>Assigned to Omar</span>
                                    </div>
                                  </div>
                                </TabsContent>
                              </Tabs>
                            </DialogContent>
                          </Dialog>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>

                {filteredIssues.length === 0 && (
                  <div className="py-8 text-center text-neutral-500 dark:text-neutral-400">
                    <p>No issues found matching the current filters.</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
        </div>
      </div>
    </div>
  );
<<<<<<< HEAD
}
=======
}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
