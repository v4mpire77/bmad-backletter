"use client";

import React, { useState, useEffect, useMemo } from "react";
import { 
  Upload, FileText, AlertTriangle, Scale, ShieldCheck, 
  Gavel, Filter, Search, Download, RefreshCw, Sparkles,
  Sun, Moon, Eye, EyeOff
} from "lucide-react";

// Import shadcn/ui components
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

// Recharts imports
import {
  BarChart as RBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
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
  const toPercent = (decimal: number) => `${(decimal * 100).toFixed(1)}%`;

  return (
    <div className={`min-h-screen transition-colors ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
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
            <div className={`px-2 py-1 rounded-full text-xs flex items-center gap-1.5 ${
              apiHealth === 'ok' ? 'bg-green-500/10 text-green-400 border border-green-500/20' :
              apiHealth === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
              'bg-gray-700 text-gray-400 border border-gray-600'
            }`}>
              <div className={`w-1.5 h-1.5 rounded-full ${
                apiHealth === 'ok' ? 'bg-green-400' :
                apiHealth === 'error' ? 'bg-red-400' :
                'bg-gray-400'
              }`} />
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
        <div className="mx-auto grid max-w-7xl grid-cols-1 gap-4 p-4 lg:grid-cols-4">
          {/* Sidebar Filters */}
          <Card className="h-fit lg:sticky lg:top-[72px]">
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

          {/* Main Grid */}
          <div className="space-y-4 lg:col-span-3">
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
                          <Badge variant={
                            issue.severity === "High" ? "destructive" : 
                            issue.severity === "Medium" ? "secondary" : 
                            "default"
                          }>
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
        </div>
      </div>
    </div>
  );
}
