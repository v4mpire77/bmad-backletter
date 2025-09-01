import React, { useMemo, useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Separator } from "@/components/ui/separator";
import {
  BarChart as RBarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip as RTooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import {
  ShieldCheck,
  Gavel,
  Scale,
  FileText,
  Upload,
  Filter,
  Search,
  Download,
  Sun,
  Moon,
  RefreshCw,
  Sparkles,
  ExternalLink,
  ClipboardCheck,
  ChevronRight,
  AlertTriangle,
} from "lucide-react";

// ------------------ Types ------------------

type IssueType = "GDPR" | "Statute" | "Case Law";

type Severity = "High" | "Medium" | "Low";

type Issue = {
  id: string;
  docId: string;
  docName: string;
  clausePath: string; // e.g., "2.1 → Data Processing → Subprocessors"
  type: IssueType;
  citation: string; // e.g., "UK GDPR Art. 28(3)(d)" or "Data Protection Act 2018 s.57" or case citation
  severity: Severity;
  confidence: number; // 0-1
  status: "Open" | "In Review" | "Resolved";
  owner?: string;
  snippet: string;
  recommendation: string;
  createdAt: string; // ISO
};

// ------------------ Mock Data ------------------

const mockIssues: Issue[] = [
  {
    id: "ISS-1001",
    docId: "DOC-ACME-MSA",
    docName: "ACME × Blackletter — Master Services Agreement (v3)",
    clausePath: "5.2 → Data Protection → International Transfers",
    type: "GDPR",
    citation: "UK GDPR Art. 44–49; DPA 2018 Part 2",
    severity: "High",
    confidence: 0.91,
    status: "Open",
    snippet:
      "Supplier may transfer Customer Personal Data outside the UK without additional safeguards.",
    recommendation:
      "Add an international transfers clause requiring adequate safeguards (e.g., UK IDTA / Addendum, SCCs + A. Transfer Risk Assessment).",
    createdAt: "2025-08-14T10:22:00Z",
  },
  {
    id: "ISS-1002",
    docId: "DOC-ACME-MSA",
    docName: "ACME × Blackletter — Master Services Agreement (v3)",
    clausePath: "5.5 → Data Protection → Subprocessors",
    type: "GDPR",
    citation: "UK GDPR Art. 28(2)-(4)",
    severity: "Medium",
    confidence: 0.84,
    status: "In Review",
    owner: "Omar",
    snippet:
      "Supplier may appoint any subprocessor without prior written authorisation.",
    recommendation:
      "Switch to prior written authorisation or at minimum provide a public subprocessor list + notice + right to object.",
    createdAt: "2025-08-14T10:23:00Z",
  },
  {
    id: "ISS-1003",
    docId: "DOC-GAD-PA",
    docName: "Government Agency — Processing Addendum",
    clausePath: "2.3 → Confidentiality",
    type: "Case Law",
    citation: "Barclays Bank plc v Various Claimants [2020] UKSC 13 (vicarious liability scope)",
    severity: "Low",
    confidence: 0.73,
    status: "Open",
    snippet:
      "The clause attempts to disclaim all liability for acts of employees and contractors.",
    recommendation:
      "Narrow liability carve-out; align with established principles on vicarious liability and statutory duties that cannot be excluded.",
    createdAt: "2025-08-15T12:01:00Z",
  },
  {
    id: "ISS-1004",
    docId: "DOC-STARTUP-DPA",
    docName: "Startup × Vendor — DPA",
    clausePath: "7.1 → Data Subject Rights",
    type: "Statute",
    citation: "Data Protection Act 2018 s.45; UK GDPR Arts. 12–23",
    severity: "High",
    confidence: 0.88,
    status: "Open",
    snippet:
      "Processor will assist with data subject requests at its discretion and may charge commercially reasonable fees.",
    recommendation:
      "Make assistance mandatory, within agreed timelines, and fee-free unless manifestly unfounded or excessive (with burden of proof).",
    createdAt: "2025-08-13T09:10:00Z",
  },
];

const mockDocs = [
  { id: "DOC-ACME-MSA", name: "ACME × Blackletter — MSA (v3)", uploadedAt: "2025-08-14" },
  { id: "DOC-GAD-PA", name: "Government Agency — Processing Addendum", uploadedAt: "2025-08-15" },
  { id: "DOC-STARTUP-DPA", name: "Startup × Vendor — DPA", uploadedAt: "2025-08-13" },
];

const gdprCoverage = [
  { article: "Art. 5 — Principles", status: "OK" },
  { article: "Art. 6 — Lawfulness", status: "OK" },
  { article: "Art. 28 — Processor", status: "GAP" },
  { article: "Art. 32 — Security", status: "OK" },
  { article: "Arts. 44–49 — Transfers", status: "GAP" },
  { article: "Art. 30 — Records", status: "Partial" },
];

const statutesCoverage = [
  { ref: "DPA 2018 Part 2", status: "Partial" },
  { ref: "PECR 2003 (as amended)", status: "OK" },
  { ref: "Consumer Rights Act 2015 (unfair terms)", status: "Review" },
];

const caseLawSignals = [
  { case: "Barclays v Various Claimants [2020] UKSC 13", weight: 0.8 },
  { case: "Lloyd v Google [2021] UKSC 50", weight: 0.7 },
  { case: "NT1 & NT2 v Google [2018] EWCA Civ 799", weight: 0.6 },
];

// ------------------ Helpers ------------------

const toPercent = (n: number) => `${Math.round(n * 100)}%`;

function downloadCSV(issues: Issue[]) {
  const headers = [
    "ID",
    "Document",
    "Clause",
    "Type",
    "Citation",
    "Severity",
    "Confidence",
    "Status",
    "Owner",
    "Snippet",
    "Recommendation",
    "CreatedAt",
  ];
  const rows = issues.map((i) => [
    i.id,
    i.docName,
    i.clausePath,
    i.type,
    i.citation,
    i.severity,
    i.confidence.toFixed(2),
    i.status,
    i.owner ?? "",
    `"${i.snippet.replaceAll('"', '""')}"`,
    `"${i.recommendation.replaceAll('"', '""')}"`,
    i.createdAt,
  ]);
  const csv = [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `compliance-issues-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(a);
  a.click();
  URL.revokeObjectURL(url);
  a.remove();
}

function riskColour(sev: Severity) {
  return sev === "High" ? "bg-red-100 text-red-700" : sev === "Medium" ? "bg-yellow-100 text-yellow-700" : "bg-green-100 text-green-700";
}

// ------------------ Dashboard ------------------

export default function LegalComplianceDashboard() {
  const [query, setQuery] = useState("");
  const [issues, setIssues] = useState<Issue[]>(mockIssues);
  const [selectedIssue, setSelectedIssue] = useState<Issue | null>(null);
  const [dark, setDark] = useState(false);
  const [typeFilter, setTypeFilter] = useState<IssueType | "All">("All");
  const [severityFilter, setSeverityFilter] = useState<Severity | "All">("All");
  const [statusFilter, setStatusFilter] = useState<"All" | Issue["status"]>("All");

  const filteredIssues = useMemo(() => {
    return issues.filter((i) => {
      const matchQuery = query
        ? [i.docName, i.citation, i.snippet, i.recommendation, i.clausePath]
            .join(" ")
            .toLowerCase()
            .includes(query.toLowerCase())
        : true;
      const matchType = typeFilter === "All" ? true : i.type === typeFilter;
      const matchSeverity = severityFilter === "All" ? true : i.severity === severityFilter;
      const matchStatus = statusFilter === "All" ? true : i.status === statusFilter;
      return matchQuery && matchType && matchSeverity && matchStatus;
    });
  }, [issues, query, typeFilter, severityFilter, statusFilter]);

  const kpis = useMemo(() => {
    const totalDocs = new Set(issues.map((i) => i.docId)).size;
    const high = issues.filter((i) => i.severity === "High").length;
    const medium = issues.filter((i) => i.severity === "Medium").length;
    const low = issues.filter((i) => i.severity === "Low").length;
    const avgConfidence = issues.reduce((a, b) => a + b.confidence, 0) / (issues.length || 1);
    return { totalDocs, high, medium, low, avgConfidence };
  }, [issues]);

  const distByType = useMemo(() => {
    const base = { GDPR: 0, Statute: 0, "Case Law": 0 } as Record<IssueType, number>;
    for (const i of filteredIssues) base[i.type]++;
    return Object.entries(base).map(([name, value]) => ({ name, value }));
  }, [filteredIssues]);

  const distBySeverity = useMemo(() => {
    const base = { High: 0, Medium: 0, Low: 0 } as Record<Severity, number>;
    for (const i of filteredIssues) base[i.severity]++;
    return [
      { name: "High", value: base["High"] },
      { name: "Medium", value: base["Medium"] },
      { name: "Low", value: base["Low"] },
    ];
  }, [filteredIssues]);

  const timeline = useMemo(() => {
    // naive bin by day
    const map = new Map<string, number>();
    for (const i of issues) {
      const key = i.createdAt.slice(0, 10);
      map.set(key, (map.get(key) ?? 0) + 1);
    }
    return Array.from(map.entries())
      .sort(([a], [b]) => (a < b ? -1 : 1))
      .map(([date, count]) => ({ date, count }));
  }, [issues]);

  function handleFakeAnalyze() {
    // Placeholder for wiring to your backend. Simulates a new issue.
    const newIssue: Issue = {
      id: `ISS-${Math.floor(Math.random() * 9000) + 1000}`,
      docId: "DOC-ACME-MSA",
      docName: "ACME × Blackletter — MSA (v3)",
      clausePath: "9.2 → Security → Breach Notification",
      type: "GDPR",
      citation: "UK GDPR Art. 33–34",
      severity: "Medium",
      confidence: 0.79,
      status: "Open",
      snippet: "Supplier shall notify without undue delay and in any case within a reasonable time.",
      recommendation: "Replace vague timing with \"within 24 hours of becoming aware\" for processors; specify details to include.",
      createdAt: new Date().toISOString(),
    };
    setIssues((prev) => [newIssue, ...prev]);
  }

  function colourForStatus(status: Issue["status"]) {
    if (status === "Resolved") return "bg-emerald-100 text-emerald-700";
    if (status === "In Review") return "bg-blue-100 text-blue-700";
    return "bg-gray-100 text-gray-700";
  }

  return (
    <div className={`${dark ? "dark" : ""}`}>
      <div className="min-h-screen bg-white text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100">
        {/* Header */}
        <div className="sticky top-0 z-40 border-b bg-white/70 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:border-neutral-800 dark:bg-neutral-950/70">
          <div className="mx-auto flex max-w-7xl items-center gap-3 p-4">
            <ShieldCheck className="h-6 w-6" />
            <h1 className="text-xl font-semibold">UK Contract Review — Compliance Analysis</h1>
            <div className="ml-auto flex items-center gap-2">
              <div className="hidden items-center gap-2 md:flex">
                <Input
                  placeholder="Search issues, citations, clauses…"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="w-[320px]"
                />
                <Button variant="outline">
                  <Search className="mr-2 h-4 w-4" /> Search
                </Button>
              </div>
              <Button variant="outline" onClick={() => setDark((d) => !d)}>
                {dark ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />} Theme
              </Button>
              <Button onClick={handleFakeAnalyze}>
                <Sparkles className="mr-2 h-4 w-4" /> Analyze
              </Button>
              <Button variant="secondary">
                <Upload className="mr-2 h-4 w-4" /> Upload
              </Button>
            </div>
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
                <Label>Jurisdiction</Label>
                <div className="flex items-center justify-between">
                  <span>United Kingdom</span>
                  <Badge variant="secondary">Default</Badge>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <Label htmlFor="gdpr-only">GDPR Focus</Label>
                <Switch id="gdpr-only" />
              </div>

              <div className="flex items-center justify-between">
                <Label htmlFor="show-closed">Hide Resolved</Label>
                <Switch
                  id="show-closed"
                  onCheckedChange={(checked) => setStatusFilter(checked ? ("Open" as const) : ("All" as const))}
                />
              </div>

              <Separator />

              <div>
                <Label className="mb-1 block">Documents</Label>
                <div className="space-y-2">
                  {mockDocs.map((d) => (
                    <div key={d.id} className="flex items-center justify-between rounded-lg border p-2 text-sm dark:border-neutral-800">
                      <div className="max-w-[70%] truncate">
                        <div className="font-medium">{d.name}</div>
                        <div className="text-xs text-neutral-500">Uploaded {d.uploadedAt}</div>
                      </div>
                      <Button variant="outline" size="sm" className="text-xs">
                        <FileText className="mr-2 h-3 w-3" /> Open
                      </Button>
                    </div>
                  ))}
                </div>
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
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
              <Card className="col-span-1">
                <CardHeader className="pb-0">
                  <CardTitle className="flex items-center gap-2 text-base"><Gavel className="h-4 w-4" /> Issues by Type</CardTitle>
                </CardHeader>
                <CardContent className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <RBarChart data={distByType}>
                      <XAxis dataKey="name" />
                      <YAxis allowDecimals={false} />
                      <RTooltip />
                      <Legend />
                      <Bar dataKey="value" name="Count" />
                    </RBarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="col-span-1">
                <CardHeader className="pb-0">
                  <CardTitle className="flex items-center gap-2 text-base"><Scale className="h-4 w-4" /> Issues by Severity</CardTitle>
                </CardHeader>
                <CardContent className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={distBySeverity} dataKey="value" nameKey="name" outerRadius={80} label />
                      <Legend />
                      <RTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="col-span-1">
                <CardHeader className="pb-0">
                  <CardTitle className="flex items-center gap-2 text-base"><FileText className="h-4 w-4" /> Findings Over Time</CardTitle>
                </CardHeader>
                <CardContent className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={timeline}>
                      <XAxis dataKey="date" />
                      <YAxis allowDecimals={false} />
                      <RTooltip />
                      <Legend />
                      <Line type="monotone" dataKey="count" name="Findings" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Coverage & Signals */}
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
              <Card className="col-span-1">
                <CardHeader className="pb-1">
                  <CardTitle className="flex items-center gap-2 text-base"><ShieldCheck className="h-4 w-4" /> GDPR Coverage Map</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {gdprCoverage.map((g) => (
                    <div key={g.article} className="flex items-center justify-between rounded-lg border p-2 text-sm dark:border-neutral-800">
                      <span>{g.article}</span>
                      <Badge variant={g.status === "OK" ? "default" : g.status === "Partial" ? "secondary" : "destructive"}>{g.status}</Badge>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="col-span-1">
                <CardHeader className="pb-1">
                  <CardTitle className="flex items-center gap-2 text-base"><Gavel className="h-4 w-4" /> Statute Coverage</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {statutesCoverage.map((s) => (
                    <div key={s.ref} className="flex items-center justify-between rounded-lg border p-2 text-sm dark:border-neutral-800">
                      <span>{s.ref}</span>
                      <Badge variant={s.status === "OK" ? "default" : s.status === "Partial" ? "secondary" : "outline"}>{s.status}</Badge>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="col-span-1">
                <CardHeader className="pb-1">
                  <CardTitle className="flex items-center gap-2 text-base"><Gavel className="h-4 w-4" /> Case Law Signals</CardTitle>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-2/3">Case</TableHead>
                        <TableHead className="text-right">Weight</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {caseLawSignals.map((c) => (
                        <TableRow key={c.case}>
                          <TableCell className="pr-2 text-sm">{c.case}</TableCell>
                          <TableCell className="text-right text-sm">{toPercent(c.weight)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </div>

            {/* Issues Table */}
            <Card>
              <CardHeader className="pb-0">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base">Flagged Issues</CardTitle>
                  <div className="flex items-center gap-2">
                    <Button variant="outline" onClick={() => downloadCSV(filteredIssues)}>
                      <Download className="mr-2 h-4 w-4" /> Export CSV
                    </Button>
                    <Button variant="outline">
                      <RefreshCw className="mr-2 h-4 w-4" /> Refresh
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-[220px]">Document</TableHead>
                        <TableHead>Clause</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Citation</TableHead>
                        <TableHead>Severity</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Confidence</TableHead>
                        <TableHead className="w-[140px]">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredIssues.map((i) => (
                        <TableRow key={i.id} className="hover:bg-neutral-50 dark:hover:bg-neutral-900">
                          <TableCell className="align-top">
                            <div className="truncate font-medium">{i.docName}</div>
                            <div className="text-xs text-neutral-500">{i.id}</div>
                          </TableCell>
                          <TableCell className="align-top text-sm">{i.clausePath}</TableCell>
                          <TableCell className="align-top">
                            <Badge variant="outline">{i.type}</Badge>
                          </TableCell>
                          <TableCell className="align-top text-sm">{i.citation}</TableCell>
                          <TableCell className="align-top">
                            <span className={`inline-flex rounded-full px-2 py-1 text-xs ${riskColour(i.severity)}`}>{i.severity}</span>
                          </TableCell>
                          <TableCell className="align-top">
                            <span className={`inline-flex rounded-full px-2 py-1 text-xs ${colourForStatus(i.status)}`}>{i.status}</span>
                          </TableCell>
                          <TableCell className="align-top text-sm">{toPercent(i.confidence)}</TableCell>
                          <TableCell className="align-top">
                            <div className="flex gap-2">
                              <Dialog>
                                <DialogTrigger asChild>
                                  <Button size="sm" variant="secondary">View</Button>
                                </DialogTrigger>
                                <DialogContent className="max-w-3xl">
                                  <DialogHeader>
                                    <DialogTitle className="flex items-center gap-2">
                                      <AlertTriangle className="h-4 w-4 text-amber-500" /> {i.docName}
                                    </DialogTitle>
                                  </DialogHeader>
                                  <div className="space-y-4">
                                    <div className="text-sm text-neutral-500">{i.clausePath}</div>
                                    <div className="flex flex-wrap items-center gap-2 text-sm">
                                      <Badge variant="outline">{i.type}</Badge>
                                      <Badge variant="secondary">{i.citation}</Badge>
                                      <span className={`rounded-full px-2 py-1 text-xs ${riskColour(i.severity)}`}>{i.severity}</span>
                                      <span className={`rounded-full px-2 py-1 text-xs ${colourForStatus(i.status)}`}>{i.status}</span>
                                      <span className="ml-auto text-xs text-neutral-500">Confidence {toPercent(i.confidence)}</span>
                                    </div>

                                    <div>
                                      <Label>Contract Snippet</Label>
                                      <div className="mt-1 rounded-lg border bg-neutral-50 p-3 text-sm dark:border-neutral-800 dark:bg-neutral-900">
                                        <mark className="rounded bg-red-100 px-1 py-0.5 text-red-800">{i.snippet}</mark>
                                      </div>
                                    </div>

                                    <div>
                                      <Label>Recommendation</Label>
                                      <div className="mt-1 rounded-lg border bg-neutral-50 p-3 text-sm dark:border-neutral-800 dark:bg-neutral-900">
                                        {i.recommendation}
                                      </div>
                                    </div>

                                    <div>
                                      <Label>Proposed Redline</Label>
                                      <Textarea placeholder="Draft a suggested clause replacement…" defaultValue={
                                        i.type === "GDPR"
                                          ? "Processor shall notify the Controller of a Personal Data Breach without undue delay and, in any case, within 24 hours of becoming aware, including the information required by UK GDPR Art. 33(3)."
                                          : "Replace with a narrow carve‑out consistent with applicable law."
                                      } />
                                    </div>

                                    <div className="flex items-center justify-end gap-2">
                                      <Button variant="outline">Assign</Button>
                                      <Button>Save</Button>
                                    </div>

                                    <Separator />

                                    <Tabs defaultValue="trace">
                                      <TabsList>
                                        <TabsTrigger value="trace">LLM Trace</TabsTrigger>
                                        <TabsTrigger value="citations">Citations</TabsTrigger>
                                        <TabsTrigger value="history">History</TabsTrigger>
                                      </TabsList>
                                      <TabsContent value="trace" className="space-y-2 text-sm">
                                        <div className="rounded-lg border p-3 dark:border-neutral-800">
                                          <div className="font-medium">Prompt (abridged)</div>
                                          <div className="text-neutral-600 dark:text-neutral-400">Extract obligations related to international transfers and assess against UK GDPR Arts. 44–49 and DPA 2018 Part 2. Return gaps and suggested fixes.</div>
                                        </div>
                                        <div className="rounded-lg border p-3 dark:border-neutral-800">
                                          <div className="font-medium">Rationale (model)</div>
                                          <div className="text-neutral-600 dark:text-neutral-400">Clause allows unrestricted transfers; missing IDTA/SCCs and TRA; recommend adding safeguard language.</div>
                                        </div>
                                      </TabsContent>
                                      <TabsContent value="citations" className="space-y-2 text-sm">
                                        <div className="rounded-lg border p-3 dark:border-neutral-800">
                                          <div className="font-medium">Primary Law</div>
                                          <ul className="list-inside list-disc text-neutral-600 dark:text-neutral-400">
                                            <li>UK GDPR Articles 28, 32, 33–34, 44–49</li>
                                            <li>Data Protection Act 2018 (selected sections)</li>
                                          </ul>
                                        </div>
                                        <div className="rounded-lg border p-3 dark:border-neutral-800">
                                          <div className="font-medium">Signals / Secondary</div>
                                          <ul className="list-inside list-disc text-neutral-600 dark:text-neutral-400">
                                            <li>ICO guidance on international transfers</li>
                                            <li>Case law relevant to liability carve‑outs</li>
                                          </ul>
                                        </div>
                                      </TabsContent>
                                      <TabsContent value="history" className="space-y-2 text-sm">
                                        <div className="text-neutral-600 dark:text-neutral-400">Created {new Date(i.createdAt).toLocaleString()}</div>
                                        <div className="text-neutral-600 dark:text-neutral-400">Owner {i.owner ?? "Unassigned"}</div>
                                      </TabsContent>
                                    </Tabs>
                                  </div>
                                </DialogContent>
                              </Dialog>

                              <Button size="sm" variant="outline" onClick={() => setSelectedIssue(i)}>Quick View</Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Drawer: Quick View */}
        <Drawer open={!!selectedIssue} onOpenChange={(o) => !o && setSelectedIssue(null)}>
          <DrawerContent className="max-h-[85vh] overflow-auto">
            <DrawerHeader>
              <DrawerTitle className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-amber-500" /> {selectedIssue?.docName}
              </DrawerTitle>
              <div className="text-xs text-neutral-500">{selectedIssue?.clausePath}</div>
            </DrawerHeader>
            <div className="grid gap-4 p-4 md:grid-cols-2">
              <div className="space-y-3">
                <div className="flex flex-wrap items-center gap-2 text-sm">
                  {selectedIssue && (
                    <>
                      <Badge variant="outline">{selectedIssue.type}</Badge>
                      <Badge variant="secondary">{selectedIssue.citation}</Badge>
                      <span className={`rounded-full px-2 py-1 text-xs ${selectedIssue ? riskColour(selectedIssue.severity) : ""}`}>{selectedIssue?.severity}</span>
                      <span className={`rounded-full px-2 py-1 text-xs ${selectedIssue ? colourForStatus(selectedIssue.status) : ""}`}>{selectedIssue?.status}</span>
                      <span className="ml-auto text-xs text-neutral-500">Confidence {selectedIssue && toPercent(selectedIssue.confidence)}</span>
                    </>
                  )}
                </div>
                <div>
                  <Label>Snippet</Label>
                  <div className="mt-1 rounded-lg border bg-neutral-50 p-3 text-sm dark:border-neutral-800 dark:bg-neutral-900">
                    {selectedIssue?.snippet}
                  </div>
                </div>
                <div>
                  <Label>Recommendation</Label>
                  <div className="mt-1 rounded-lg border bg-neutral-50 p-3 text-sm dark:border-neutral-800 dark:bg-neutral-900">
                    {selectedIssue?.recommendation}
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <Label>Proposed Redline</Label>
                  <Textarea placeholder="Add your redline suggestion…" />
                </div>
                <div className="flex items-center justify-end gap-2">
                  <Button variant="outline" onClick={() => setSelectedIssue(null)}>Close</Button>
                  <Button>Save</Button>
                </div>
              </div>
            </div>
            <DrawerFooter>
              <div className="text-xs text-neutral-500">This tool surfaces potential issues for legal review. It does not constitute legal advice.</div>
              <DrawerClose asChild>
                <Button variant="secondary">Done</Button>
              </DrawerClose>
            </DrawerFooter>
          </DrawerContent>
        </Drawer>

        {/* Footer */}
        <div className="border-t p-4 text-center text-xs text-neutral-500 dark:border-neutral-800">
          © {new Date().getFullYear()} Blackletter — UK Contract Review & Compliance Checker
        </div>
      </div>
    </div>
  );
}

// ------------------ Wiring Guide (dev notes) ------------------
// Hook these UI actions to your backend:
// - Upload: POST /api/docs (multipart)
// - Analyze: POST /api/analyze { docId | text } → Issue[] with {citation, type, severity, confidence, recommendation, clausePath}
// - Refresh: GET /api/issues?filters
// - Export CSV: GET /api/export?format=csv (or use the frontend util provided)
// - Citations: GET /api/citations?issueId → {primaryLaw: string[], guidance: string[]}
// - Coverage maps: GET /api/gdpr-coverage?docId; GET /api/statute-coverage?docId
// - Case law signals: GET /api/caselaw?docId → {case, weight}[]
// - Redlines save: POST /api/redlines {issueId, text}
//
// Data Model (Issue):
// {
//   id: string,
//   docId: string,
//   docName: string,
//   clausePath: string,
//   type: "GDPR" | "Statute" | "Case Law",
//   citation: string,
//   severity: "High" | "Medium" | "Low",
//   confidence: number,
//   status: "Open" | "In Review" | "Resolved",
//   owner?: string,
//   snippet: string,
//   recommendation: string,
//   createdAt: ISO string
// }
//
// Notes:
// - The dashboard is jurisdiction-aware but seeded for UK (UK GDPR, DPA 2018, PECR, CRA 2015, relevant case law).
// - Replace mock data with your analyzer output. Ensure each issue has a stable id for diffing.
// - Use server-side pagination for large result sets.
// - For true diffing, integrate a code/diff view (e.g., react-diff-viewer) in the Dialog.
// - Add auth/roles to gate who can resolve/assign issues.
// - Consider streaming analyze results over SSE/WebSocket for real-time UX.
