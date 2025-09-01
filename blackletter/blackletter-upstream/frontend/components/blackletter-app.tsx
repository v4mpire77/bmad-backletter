import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Shield,
  AlertTriangle,
  Clock,
  CheckCircle,
  Upload,
  Menu,
  Bell,
  Search,
  ChevronRight,
  File,
  Eye,
  Plus,
  RotateCcw,
  BarChart3,
  Users,
  Settings,
  Zap,
  Target,
  Activity,
  Moon,
  Filter,
  Download,
  Share,
  Edit,
  MessageSquare,
  Calendar,
  Briefcase,
  FileSignature,
  Archive,
  AlertCircle,
  TrendingUp,
  Database,
  UserCheck,
  Lock,
  Globe,
  History,
  Tag,
  Workflow,
  Lightbulb,
  Star,
  MoreHorizontal,
  BookOpen,
  ShieldCheck,
  UserX,
  Timer,
  ExternalLink,
  FileX,
  Trash2,
  Scale,
  Building2,
  Gavel,
  Crown,
  MapPin,
  AlertOctagon,
  FileCheck,
  Fingerprint,
  Key,
  RefreshCw,
  FileOutput,
  Ban,
} from 'lucide-react'; // Importing all necessary icons from lucide-react

// Mock data with legal-specific content
const recentContracts = [
  {
    id: 1,
    name: "Master Service Agreement - Microsoft Corp",
    status: "Under Review",
    riskLevel: "high",
    uploadDate: "2024-01-15",
    issues: 8,
    type: "MSA",
    priority: "urgent",
    assignee: "Sarah Chen",
    deadline: "2024-01-20",
    aiConfidence: 94,
    redlines: 12,
    value: "$2.4M",
    lastActivity: "2 hours ago",
    department: "Technology",
    tags: ["High Value", "Fortune 500", "Multi-year"]
  },
  {
    id: 2,
    name: "Employment Agreement - Senior Developer",
    status: "Approved",
    riskLevel: "low",
    uploadDate: "2024-01-14",
    issues: 0,
    type: "Employment",
    priority: "normal",
    assignee: "Mike Torres",
    deadline: "2024-01-16",
    aiConfidence: 98,
    redlines: 3,
    value: "$180K",
    lastActivity: "1 day ago",
    department: "Human Resources",
    tags: ["Remote Work", "Senior Level"]
  },
  {
    id: 3,
    name: "SaaS License Agreement - Salesforce",
    status: "Needs Attention",
    riskLevel: "critical",
    uploadDate: "2024-01-13",
    issues: 15,
    type: "Software License",
    priority: "urgent",
    assignee: "Lisa Park",
    deadline: "2024-01-18",
    aiConfidence: 89,
    redlines: 23,
    value: "$500K",
    lastActivity: "30 minutes ago",
    department: "Technology",
    tags: ["Software", "Enterprise", "Data Processing"]
  },
  {
    id: 4,
    name: "NDA - Venture Capital Firm",
    status: "Processing",
    riskLevel: "medium",
    uploadDate: "2024-01-12",
    issues: 3,
    type: "NDA",
    priority: "normal",
    assignee: "David Kim",
    deadline: "2024-01-19",
    aiConfidence: 92,
    redlines: 5,
    value: "N/A",
    lastActivity: "4 hours ago",
    department: "Finance",
    tags: ["Confidential", "Investment"]
  },
  {
    id: 5,
    name: "Supplier Agreement - Global Manufacturing Ltd",
    status: "Under Review",
    riskLevel: "medium",
    uploadDate: "2024-01-11",
    issues: 6,
    type: "Supply Chain",
    priority: "normal",
    assignee: "Emma Wilson",
    deadline: "2024-01-22",
    aiConfidence: 91,
    redlines: 8,
    value: "$1.2M",
    lastActivity: "6 hours ago",
    department: "Operations",
    tags: ["International", "Supply Chain", "Manufacturing"]
  },
  {
    id: 6,
    name: "Partnership Agreement - FinTech Startup",
    status: "Draft",
    riskLevel: "high",
    uploadDate: "2024-01-10",
    issues: 12,
    type: "Partnership",
    priority: "urgent",
    assignee: "Alex Rodriguez",
    deadline: "2024-01-17",
    aiConfidence: 87,
    redlines: 18,
    value: "$3.1M",
    lastActivity: "1 hour ago",
    department: "Business Development",
    tags: ["Strategic", "FinTech", "Revenue Share"]
  }
];

const stats = [
  { 
    label: "Contracts Processed", 
    value: "3,247", 
    change: "+18%", 
    period: "this month",
    icon: FileText,
    color: "from-purple-500 to-purple-600"
  },
  { 
    label: "AI Risk Score", 
    value: "2.1/10", 
    change: "-24%", 
    period: "avg this month",
    icon: AlertTriangle,
    color: "from-red-500 to-red-600"
  },
  { 
    label: "Review Velocity", 
    value: "4.2h", 
    change: "-31%", 
    period: "avg turnaround",
    icon: Clock,
    color: "from-orange-500 to-orange-600"
  },
  { 
    label: "Contract Value", 
    value: "$47.2M", 
    change: "+12%", 
    period: "under management",
    icon: TrendingUp,
    color: "from-green-500 to-green-600"
  }
];

// Risk level configurations
type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

const getRiskConfig = (level: string) => {
  const configs: Record<RiskLevel, any> = {
    low: { 
      color: 'text-green-400 bg-green-500/10 border-green-500/30',
      icon: Shield,
      label: 'Low Risk',
      glow: 'shadow-green-500/20'
    },
    medium: { 
      color: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
      icon: AlertTriangle,
      label: 'Medium Risk',
      glow: 'shadow-yellow-500/20'
    },
    high: { 
      color: 'text-orange-400 bg-orange-500/10 border-orange-500/30',
      icon: AlertTriangle,
      label: 'High Risk',
      glow: 'shadow-orange-500/20'
    },
    critical: { 
      color: 'text-red-400 bg-red-500/10 border-red-500/30',
      icon: Zap,
      label: 'Critical',
      glow: 'shadow-red-500/20'
    }
  };
  return configs[level as RiskLevel] || configs.medium;
};

type StatusType = "Under Review" | "Approved" | "Needs Attention" | "Processing";

const getStatusConfig = (status: string) => {
  const configs: Record<StatusType, any> = {
    "Under Review": { 
      color: 'text-blue-400 bg-blue-500/10 border-blue-500/30', 
      icon: Clock,
      glow: 'shadow-blue-500/20'
    },
    "Approved": { 
      color: 'text-green-400 bg-green-500/10 border-green-500/30', 
      icon: CheckCircle,
      glow: 'shadow-green-500/20'
    },
    "Needs Attention": { 
      color: 'text-red-400 bg-red-500/10 border-red-500/30', 
      icon: AlertTriangle,
      glow: 'shadow-red-500/20'
    },
    "Processing": { 
      color: 'text-purple-400 bg-purple-500/10 border-purple-500/30', 
      icon: RotateCcw,
      glow: 'shadow-purple-500/20'
    }
  };
  return configs[status as StatusType] || configs["Under Review"];
};

// Components
const StatCard = ({ stat }: { stat: any }) => {
  const Icon = stat.icon;
  
  return (
    <div className="bg-gray-900/90 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50 hover:border-gray-700/50 transition-all duration-300 hover:shadow-xl group">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg bg-gradient-to-r ${stat.color} bg-opacity-10`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div className="text-right">
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${stat.change.startsWith('+') ? 'text-green-400 bg-green-500/10' : 'text-red-400 bg-red-500/10'}`}>
            {stat.change}
          </span>
        </div>
      </div>
      
      <div>
        <p className="text-sm font-medium text-gray-400 mb-2">{stat.label}</p>
        <p className="text-3xl font-bold text-white mb-1">{stat.value}</p>
        <p className="text-xs text-gray-500">{stat.period}</p>
      </div>
    </div>
  );
};

const ContractCard = ({ contract, onSelect }: { contract: any; onSelect: (contract: any) => void }) => {
  const riskConfig = getRiskConfig(contract.riskLevel);
  const statusConfig = getStatusConfig(contract.status);
  const RiskIcon = riskConfig.icon;
  const StatusIcon = statusConfig.icon;
  const isUrgent = contract.priority === 'urgent';
  const isNearDeadline = new Date(contract.deadline).getTime() - new Date().getTime() < 5 * 24 * 60 * 60 * 1000; // 5 days

  return (
    <div 
      className={`bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border transition-all duration-300 cursor-pointer group hover:shadow-xl hover:scale-105 ${
        isUrgent ? 'border-red-500/30 hover:border-red-500/50 shadow-lg shadow-red-500/5' : 'border-gray-800/50 hover:border-gray-700/50'
      }`}
      onClick={() => onSelect && onSelect(contract)}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-3 flex-1">
          <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
            <FileSignature className="w-5 h-5 text-purple-400" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2 mb-1">
              <h3 className="font-semibold text-white truncate group-hover:text-purple-400 transition-colors">
                {contract.name}
              </h3>
              {isUrgent && (
                <span className="text-xs font-medium px-2 py-0.5 bg-red-500/20 text-red-400 rounded-full">
                  URGENT
                </span>
              )}
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-400">
              <span>{contract.type}</span>
              <span>•</span>
              <span>{contract.value}</span>
              <span>•</span>
              <span>AI: {contract.aiConfidence}%</span>
            </div>
          </div>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-purple-400 transition-colors" />
      </div>
      
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium border ${statusConfig.color}`}>
            <StatusIcon className="w-3 h-3" />
            <span>{contract.status}</span>
          </div>
          <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium border ${riskConfig.color}`}>
            <RiskIcon className="w-3 h-3" />
            <span>{riskConfig.label}</span>
          </div>
        </div>
      </div>
      
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center space-x-4 text-gray-500">
          <span className="flex items-center space-x-1">
            <UserCheck className="w-3 h-3" />
            <span>{contract.assignee}</span>
          </span>
          <span className="flex items-center space-x-1">
            <Calendar className="w-3 h-3" />
            <span className={isNearDeadline ? 'text-red-400' : ''}>
              {new Date(contract.deadline).toLocaleDateString()}
            </span>
          </span>
        </div>
        <span className={`font-medium ${contract.issues > 0 ? 'text-red-400' : 'text-green-400'}`}>
          {contract.redlines} redlines • {contract.issues} issues
        </span>
      </div>
    </div>
  );
};

const UploadArea = ({ onUpload }: { onUpload: (files: File[]) => void }) => {
  const [dragOver, setDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const simulateUpload = async () => {
    setIsUploading(true);
    setUploadProgress(0);
    
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 100));
      setUploadProgress(i);
    }
    
    setTimeout(() => {
      setIsUploading(false);
      setUploadProgress(0);
    }, 1000);
  };

  const handleDrop = async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    await simulateUpload();
    onUpload(files);
  };

  const handleClick = async () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;
    input.accept = '.pdf,.docx,.txt,.doc';
    input.onchange = async (e) => {
      await simulateUpload();
      const target = e.target as HTMLInputElement;
      onUpload(Array.from(target.files || []));
    };
    input.click();
  };

  if (isUploading) {
    return (
      <div className="relative border-2 border-purple-400 bg-purple-500/10 rounded-2xl p-10 text-center backdrop-blur-sm shadow-lg shadow-purple-500/20">
        <div className="mx-auto w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 animate-pulse">
          <RotateCcw className="w-8 h-8 text-white animate-spin" />
        </div>
        <h3 className="text-xl font-bold text-white mb-3">Processing Upload</h3>
        <p className="text-purple-300 mb-6">AI analysis in progress...</p>
        <div className="w-full bg-gray-800 rounded-full h-2 mb-4">
          <div 
            className="bg-gradient-to-r from-purple-500 to-purple-400 h-2 rounded-full transition-all duration-300"
            style={{width: `${uploadProgress}%`}}
          />
        </div>
        <p className="text-sm text-purple-400">{uploadProgress}% complete</p>
      </div>
    );
  }

  return (
    <div 
      className={`relative border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-300 cursor-pointer backdrop-blur-sm ${
        dragOver 
          ? 'border-purple-400 bg-purple-500/10 shadow-lg shadow-purple-500/20 scale-105' 
          : 'border-gray-700 hover:border-gray-600 bg-gray-900/20 hover:scale-105'
      }`}
      onDrop={handleDrop}
              onDragOver={(e: React.DragEvent<HTMLDivElement>) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onClick={handleClick}
    >
      <div className={`mx-auto w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 shadow-lg shadow-purple-500/25 transition-transform ${dragOver ? 'scale-110' : ''}`}>
        <Upload className="w-8 h-8 text-white" />
      </div>
      <h3 className="text-xl font-bold text-white mb-3">Upload Contract</h3>
      <p className="text-gray-400 mb-6 text-lg">Drag and drop documents for AI-powered analysis</p>
      <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-purple-800 transition-all duration-300 shadow-lg shadow-purple-500/25 hover:scale-105">
        <Plus className="w-4 h-4 mr-2" />
        Select Files
      </div>
      <p className="text-xs text-gray-500 mt-4">PDF, DOCX, DOC, TXT • Up to 50MB • 256-bit encryption</p>
      {dragOver && (
        <div className="absolute inset-0 rounded-2xl bg-purple-500/20 border-2 border-purple-400 flex items-center justify-center">
          <div className="text-purple-300 text-lg font-semibold">Drop files here</div>
        </div>
      )}
    </div>
  );
};

const Sidebar = ({ activeTab, setActiveTab }: { activeTab: string; setActiveTab: (tab: string) => void }) => {
  const navigation = [
    { name: 'Dashboard', icon: BarChart3, key: 'dashboard' },
    { name: 'Contracts', icon: FileSignature, key: 'contracts' },
    { name: 'Review Queue', icon: Clock, key: 'queue' },
    { name: 'Templates', icon: File, key: 'templates' },
    { name: 'AI Insights', icon: Zap, key: 'insights' },
    { name: 'GDPR Centre', icon: ShieldCheck, key: 'gdpr' },
    { name: 'Compliance', icon: Shield, key: 'compliance' },
    { name: 'UK Legal Hub', icon: Crown, key: 'uk-legal' },
    { name: 'Workflows', icon: Workflow, key: 'workflows' },
    { name: 'Reporting', icon: TrendingUp, key: 'reports' },
    { name: 'Team', icon: Users, key: 'team' },
    { name: 'Settings', icon: Settings, key: 'settings' }
  ];

  return (
    <div className="w-72 bg-gray-950/95 backdrop-blur-xl border-r border-gray-800/50 flex flex-col h-full">
      <div className="p-8">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-gradient-to-r from-gray-700 to-gray-800 rounded-lg flex items-center justify-center border border-gray-700">
            <FileText className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="text-2xl font-bold text-white">
              Blackletter
            </span>
            <p className="text-xs text-gray-500 tracking-wider">CONTRACT INTELLIGENCE</p>
          </div>
        </div>
      </div>
      
      <nav className="flex-1 px-6">
        <ul className="space-y-2">
          {navigation.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.key;
            return (
              <li key={item.key}>
                <button
                  onClick={() => setActiveTab(item.key)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-all duration-200 font-medium ${
                    isActive 
                      ? 'bg-gray-800 text-white border border-gray-700' 
                      : 'text-gray-400 hover:bg-gray-900/50 hover:text-white'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>
      
      <div className="p-6">
        <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-8 h-8 bg-green-500/10 rounded-lg flex items-center justify-center border border-green-500/20">
              <Activity className="w-4 h-4 text-green-400" />
            </div>
            <span className="font-semibold text-green-400">System Health</span>
          </div>
          <div className="text-2xl font-bold text-green-400 mb-2">99.9%</div>
          <p className="text-xs text-green-300/70">All systems operational</p>
          <div className="w-full bg-gray-800 rounded-full h-1.5 mt-3">
            <div className="bg-gradient-to-r from-green-500 to-green-400 h-1.5 rounded-full" style={{width: '99.9%'}}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

const Header = ({ activeTab }: { activeTab: string }) => {
  const getPageTitle = (tab: string) => {
    const titles: Record<string, string> = {
      dashboard: 'Dashboard',
      contracts: 'Contract Management',
      queue: 'Review Queue',
      templates: 'Template Library',
      insights: 'AI Insights',
      gdpr: 'GDPR Centre',
      compliance: 'Compliance Center',
      'uk-legal': 'UK Legal Hub',
      workflows: 'Workflow Automation',
      reports: 'Analytics & Reports',
      team: 'Team Management',
      settings: 'Settings'
    };
    return titles[tab] || 'Dashboard';
  };

  return (
    <header className="bg-gray-950/95 backdrop-blur-xl border-b border-gray-800/50 px-8 py-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <h1 className="text-2xl font-bold text-white">{getPageTitle(activeTab)}</h1>
          <div className="flex items-center space-x-2 px-3 py-1 bg-green-500/10 rounded-full border border-green-500/20">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-xs text-green-400 font-medium">LIVE</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-6">
          <div className="relative">
            <Search className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 transform -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search contracts, clauses, parties..."
              className="w-96 pl-12 pr-4 py-3 bg-gray-900/50 border border-gray-800/50 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all outline-none backdrop-blur-sm"
            />
          </div>
          
          <div className="flex items-center space-x-3">
            <button className="p-2 text-gray-400 hover:text-white transition-colors relative">
              <MessageSquare className="w-5 h-5" />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full"></span>
            </button>
            
            <button className="p-2 text-gray-400 hover:text-white transition-colors relative">
              <Bell className="w-5 h-5" />
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-xs text-white font-bold">7</span>
              </span>
            </button>

            <div className="w-px h-6 bg-gray-700"></div>

            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 bg-gradient-to-r from-purple-600 to-purple-700 rounded-full flex items-center justify-center">
                <span className="text-sm font-bold text-white">AC</span>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold text-white">Alex Chen</p>
                <p className="text-xs text-gray-400">Senior Legal Counsel</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

// GDPR Content Component
const GDPRContent = () => {
  const [dataRequests] = useState([
    { id: 1, type: 'Right to Access', requestor: 'John Smith', status: 'Pending', deadline: '2024-02-15' },
    { id: 2, type: 'Right to Erasure', requestor: 'Sarah Jones', status: 'In Progress', deadline: '2024-02-18' },
    { id: 3, type: 'Data Portability', requestor: 'Mike Chen', status: 'Completed', deadline: '2024-02-10' }
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">GDPR Data Protection Centre</h2>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 px-3 py-1 bg-green-500/10 rounded-full border border-green-500/20">
            <ShieldCheck className="w-4 h-4 text-green-400" />
            <span className="text-xs text-green-400 font-medium">GDPR COMPLIANT</span>
          </div>
          <button className="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors">
            <AlertTriangle className="w-4 h-4 mr-2" />
            Report Breach
          </button>
        </div>
      </div>

      {/* GDPR Dashboard Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
              <Fingerprint className="w-5 h-5 text-blue-400" />
            </div>
            <h3 className="font-semibold text-white">Data Classification</h3>
          </div>
          <div className="text-2xl font-bold text-blue-400 mb-1">2,847</div>
          <div className="text-xs text-gray-400">Personal data records</div>
          <div className="mt-3 text-xs text-green-400">+12% classified this month</div>
        </div>

        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-green-500/10 rounded-lg border border-green-500/20">
              <UserCheck className="w-5 h-5 text-green-400" />
            </div>
            <h3 className="font-semibold text-white">Active Consents</h3>
          </div>
          <div className="text-2xl font-bold text-green-400 mb-1">1,234</div>
          <div className="text-xs text-gray-400">Valid consent records</div>
          <div className="mt-3 text-xs text-yellow-400">47 expiring soon</div>
        </div>

        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-orange-500/10 rounded-lg border border-orange-500/20">
              <Timer className="w-5 h-5 text-orange-400" />
            </div>
            <h3 className="font-semibold text-white">Retention Policies</h3>
          </div>
          <div className="text-2xl font-bold text-orange-400 mb-1">156</div>
          <div className="text-xs text-gray-400">Auto-expire rules</div>
          <div className="mt-3 text-xs text-red-400">23 documents expiring today</div>
        </div>

        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
              <BarChart3 className="w-5 h-5 text-purple-400" />
            </div>
            <h3 className="font-semibold text-white">Risk Score</h3>
          </div>
          <div className="text-2xl font-bold text-purple-400 mb-1">2.3/10</div>
          <div className="text-xs text-gray-400">GDPR compliance risk</div>
          <div className="mt-3 text-xs text-green-400">-15% from last month</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Data Subject Requests */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
                <FileOutput className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="text-lg font-bold text-white">Data Subject Requests</h3>
            </div>
            <button className="text-blue-400 hover:text-blue-300 text-sm font-medium">
              View All
            </button>
          </div>

          <div className="space-y-4">
            {dataRequests.map((request) => (
              <div key={request.id} className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg border border-gray-700/30">
                <div>
                  <div className="font-medium text-white mb-1">{request.type}</div>
                  <div className="text-sm text-gray-400">{request.requestor}</div>
                </div>
                <div className="text-right">
                  <div className={`text-sm font-medium mb-1 ${
                    request.status === 'Completed' ? 'text-green-400' :
                    request.status === 'In Progress' ? 'text-yellow-400' : 'text-red-400'
                  }`}>
                    {request.status}
                  </div>
                  <div className="text-xs text-gray-500">Due: {request.deadline}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* GDPR Tools */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
              <Zap className="w-5 h-5 text-purple-400" />
            </div>
            <h3 className="text-lg font-bold text-white">GDPR Tools</h3>
          </div>

          <div className="grid grid-cols-1 gap-4">
            <button className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg border border-gray-700/30 hover:border-gray-600/50 transition-colors">
              <div className="flex items-center space-x-3">
                <FileCheck className="w-5 h-5 text-green-400" />
                <div>
                  <div className="font-medium text-white">Generate DPIA</div>
                  <div className="text-sm text-gray-400">Data Protection Impact Assessment</div>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-500" />
            </button>

            <button className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg border border-gray-700/30 hover:border-gray-600/50 transition-colors">
              <div className="flex items-center space-x-3">
                <Trash2 className="w-5 h-5 text-red-400" />
                <div>
                  <div className="font-medium text-white">Right to Erasure</div>
                  <div className="text-sm text-gray-400">Complete data deletion with audit</div>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-500" />
            </button>

            <button className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg border border-gray-700/30 hover:border-gray-600/50 transition-colors">
              <div className="flex items-center space-x-3">
                <Download className="w-5 h-5 text-blue-400" />
                <div>
                  <div className="font-medium text-white">Data Export</div>
                  <div className="text-sm text-gray-400">Machine-readable data portability</div>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-500" />
            </button>

            <button className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg border border-gray-700/30 hover:border-gray-600/50 transition-colors">
              <div className="flex items-center space-x-3">
                <Key className="w-5 h-5 text-yellow-400" />
                <div>
                  <div className="font-medium text-white">Consent Manager</div>
                  <div className="text-sm text-gray-400">Track and manage all consents</div>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-500" />
            </button>
          </div>
        </div>
      </div>

      {/* Breach Response Dashboard */}
      <div className="bg-gradient-to-r from-red-900/20 to-orange-900/20 backdrop-blur-sm rounded-xl p-6 border border-red-800/30">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-red-500/10 rounded-lg border border-red-500/20">
              <AlertOctagon className="w-6 h-6 text-red-400" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Breach Response Centre</h3>
              <p className="text-sm text-gray-400">72-hour notification compliance</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-green-400">0</div>
            <div className="text-xs text-gray-400">Active breaches</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-gray-900/30 rounded-lg border border-gray-700/30">
            <div className="text-xl font-bold text-green-400 mb-1">100%</div>
            <div className="text-xs text-gray-400">On-time notifications</div>
          </div>
          <div className="text-center p-4 bg-gray-900/30 rounded-lg border border-gray-700/30">
            <div className="text-xl font-bold text-blue-400 mb-1">47</div>
            <div className="text-xs text-gray-400">Historical breaches</div>
          </div>
          <div className="text-center p-4 bg-gray-900/30 rounded-lg border border-gray-700/30">
            <div className="text-xl font-bold text-purple-400 mb-1">£0</div>
            <div className="text-xs text-gray-400">GDPR fines avoided</div>
          </div>
        </div>
      </div>
    </div>
  );
};

// UK Legal Hub Component
const UKLegalContent = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h2 className="text-xl font-bold text-white">UK Legal Hub</h2>
          <div className="flex items-center space-x-2 px-3 py-1 bg-blue-500/10 rounded-full border border-blue-500/20">
            <Crown className="w-4 h-4 text-blue-400" />
            <span className="text-xs text-blue-400 font-medium">UK JURISDICTION</span>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <button className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
            <ExternalLink className="w-4 h-4 mr-2" />
            HMCTS Portal
          </button>
        </div>
      </div>

      {/* Integration Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
              <Building2 className="w-5 h-5 text-blue-400" />
            </div>
            <h3 className="font-semibold text-white">ICO Integration</h3>
          </div>
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-green-400 font-medium">Connected</span>
          </div>
          <div className="text-xs text-gray-400 mb-4">Last sync: 2 hours ago</div>
          <button className="text-blue-400 hover:text-blue-300 text-sm font-medium">
            Submit Breach Report →
          </button>
        </div>

        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
              <Gavel className="w-5 h-5 text-purple-400" />
            </div>
            <h3 className="font-semibold text-white">HMCTS Filing</h3>
          </div>
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-green-400 font-medium">Active</span>
          </div>
          <div className="text-xs text-gray-400 mb-4">Electronic filing enabled</div>
          <button className="text-purple-400 hover:text-purple-300 text-sm font-medium">
            File Documents →
          </button>
        </div>

        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-green-500/10 rounded-lg border border-green-500/20">
              <Scale className="w-5 h-5 text-green-400" />
            </div>
            <h3 className="font-semibold text-white">Legal Aid</h3>
          </div>
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
            <span className="text-sm text-yellow-400 font-medium">3 Pending</span>
          </div>
          <div className="text-xs text-gray-400 mb-4">Applications in review</div>
          <button className="text-green-400 hover:text-green-300 text-sm font-medium">
            Manage Applications →
          </button>
        </div>
      </div>

      {/* UK-Specific Templates */}
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-red-500/10 rounded-lg border border-red-500/20">
              <FileText className="w-5 h-5 text-red-400" />
            </div>
            <h3 className="text-lg font-bold text-white">UK Legal Templates</h3>
          </div>
          <button className="text-red-400 hover:text-red-300 text-sm font-medium">
            View All Templates
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { name: 'Employment Contract (UK)', compliance: 'GDPR + UK Employment Law', icon: Users, usage: 89 },
            { name: 'Data Processing Agreement', compliance: 'GDPR Article 28', icon: ShieldCheck, usage: 156 },
            { name: 'Privacy Notice Template', compliance: 'GDPR Articles 13-14', icon: Eye, usage: 234 },
            { name: 'Consent Form (GDPR)', compliance: 'GDPR Article 7', icon: UserCheck, usage: 67 },
            { name: 'Subject Access Request', compliance: 'GDPR Article 15', icon: FileOutput, usage: 43 },
            { name: 'Data Breach Notification', compliance: 'GDPR Article 33', icon: AlertTriangle, usage: 12 }
          ].map((template, index) => {
            const Icon = template.icon;
            return (
              <div key={index} className="p-4 bg-gray-800/30 rounded-lg border border-gray-700/30 hover:border-gray-600/50 transition-colors cursor-pointer">
                <div className="flex items-center space-x-3 mb-3">
                  <Icon className="w-5 h-5 text-blue-400" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-white text-sm truncate">{template.name}</div>
                    <div className="text-xs text-gray-400">{template.compliance}</div>
                  </div>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-green-400">Used {template.usage}x</span>
                  <button className="text-blue-400 hover:text-blue-300">Use Template</button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

const DashboardContent = ({ onUpload, onContractSelect, searchQuery }: { onUpload: (files: File[]) => void; onContractSelect: (contract: any) => void; searchQuery: string }) => (
  <div className="space-y-8">
    {/* Quick Actions Bar */}
    <div className="flex items-center justify-between p-6 bg-gray-900/50 backdrop-blur-sm rounded-xl border border-gray-800/50">
      <div>
        <h2 className="text-xl font-bold text-white mb-2">
          Welcome back, Alex
        </h2>
        <p className="text-gray-400">
          You have <span className="text-purple-400 font-semibold">7 contracts</span> pending review and <span className="text-red-400 font-semibold">3 urgent items</span> requiring attention.
        </p>
      </div>
      <div className="flex items-center space-x-3">
        <button className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors hover:scale-105">
          <Plus className="w-4 h-4 mr-2" />
          New Contract
        </button>
        <button className="inline-flex items-center px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg font-medium transition-colors hover:scale-105">
          <Calendar className="w-4 h-4 mr-2" />
          Schedule Review
        </button>
      </div>
    </div>

    {/* Stats Grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <StatCard key={index} stat={stat} />
      ))}
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Upload Area */}
      <div className="lg:col-span-1">
        <UploadArea onUpload={onUpload} />
      </div>

      {/* Recent Contracts */}
      <div className="lg:col-span-2">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-white">Recent Activity</h2>
          <div className="flex items-center space-x-3">
            <button className="text-purple-400 hover:text-purple-300 font-medium transition-colors">
              View All
            </button>
            <div className="w-px h-4 bg-gray-700"></div>
            <button className="p-2 text-gray-400 hover:text-white transition-colors">
              <Filter className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className="space-y-4">
          {recentContracts.map((contract) => (
            <ContractCard key={contract.id} contract={contract} onSelect={onContractSelect} />
          ))}
        </div>
      </div>
    </div>

    {/* Popular Features Section */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50 hover:border-gray-700/50 transition-all cursor-pointer hover:scale-105">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
            <Zap className="w-6 h-6 text-blue-400" />
          </div>
          <h3 className="text-lg font-semibold text-white">AI Contract Review</h3>
        </div>
        <p className="text-gray-400 text-sm mb-4">Automated risk assessment and clause analysis powered by machine learning</p>
        <button className="text-blue-400 hover:text-blue-300 text-sm font-medium">
          Start Analysis →
        </button>
      </div>

      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50 hover:border-gray-700/50 transition-all cursor-pointer hover:scale-105">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-green-500/10 rounded-lg border border-green-500/20">
            <FileSignature className="w-6 h-6 text-green-400" />
          </div>
          <h3 className="text-lg font-semibold text-white">Digital Signatures</h3>
        </div>
        <p className="text-gray-400 text-sm mb-4">Secure e-signature workflow with DocuSign and Adobe Sign integration</p>
        <button className="text-green-400 hover:text-green-300 text-sm font-medium">
          Send for Signing →
        </button>
      </div>

      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50 hover:border-gray-700/50 transition-all cursor-pointer hover:scale-105">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-orange-500/10 rounded-lg border border-orange-500/20">
            <Workflow className="w-6 h-6 text-orange-400" />
          </div>
          <h3 className="text-lg font-semibold text-white">Approval Workflows</h3>
        </div>
        <p className="text-gray-400 text-sm mb-4">Automated routing and approval processes with customizable rules</p>
        <button className="text-orange-400 hover:text-orange-300 text-sm font-medium">
          Configure Workflow →
        </button>
      </div>
    </div>
  </div>
);

// Review Queue Component
const ReviewQueueContent = ({ onContractSelect, searchQuery }: { onContractSelect: (contract: any) => void, searchQuery: string }) => (
  <div className="space-y-6">
    <div className="flex items-center justify-between">
      <h2 className="text-xl font-bold text-white">Review Queue</h2>
      <div className="flex items-center space-x-3">
        <button className="inline-flex items-center px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-medium transition-colors">
          <Clock className="w-4 h-4 mr-2" />
          View All Pending
        </button>
      </div>
    </div>
    
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      {recentContracts
        .filter(contract => contract.status === "Under Review" || contract.status === "Needs Attention")
        .map((contract, index) => (
          <ContractCard key={`queue-${contract.id}-${index}`} contract={contract} onSelect={onContractSelect} />
        ))}
    </div>
  </div>
);

// AI Insights Component
const AIInsightsContent = () => (
  <div className="space-y-6">
    <div className="flex items-center justify-between">
      <h2 className="text-xl font-bold text-white">AI Insights & Analytics</h2>
      <div className="flex items-center space-x-3">
        <button className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
          <BarChart3 className="w-4 h-4 mr-2" />
          Export Report
        </button>
      </div>
    </div>
    
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
        <h3 className="text-lg font-semibold text-white mb-4">Risk Trends</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">High Risk Contracts</span>
            <span className="text-red-400 font-semibold">+12%</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-400">GDPR Compliance</span>
            <span className="text-green-400 font-semibold">-8%</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Data Processing</span>
            <span className="text-yellow-400 font-semibold">+5%</span>
          </div>
        </div>
      </div>
      
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800/50">
        <h3 className="text-lg font-semibold text-white mb-4">AI Performance</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Accuracy Rate</span>
            <span className="text-green-400 font-semibold">94.2%</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Processing Time</span>
            <span className="text-blue-400 font-semibold">2.1 min</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Issues Detected</span>
            <span className="text-orange-400 font-semibold">1,247</span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// All other components continue as before...
const ContractsContent = ({ onContractSelect, searchQuery }: { onContractSelect: (contract: any) => void; searchQuery: string }) => (
  <div className="space-y-6">
    <div className="flex items-center justify-between">
      <h2 className="text-xl font-bold text-white">Contract Repository</h2>
      <div className="flex items-center space-x-3">
        <button className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors">
          <Plus className="w-4 h-4 mr-2" />
          New Contract
        </button>
      </div>
    </div>
    
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      {recentContracts.map((contract, index) => (
        <ContractCard key={`${contract.id}-${index}`} contract={contract} onSelect={onContractSelect} />
      ))}
    </div>
  </div>
);

// Main App Component
export default function BlackletterApp() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [searchQuery, setSearchQuery] = useState('');
  const [notifications] = useState([]);

  const handleUpload = (files: File[]) => {
    console.log('Uploading files:', files);
    // Simulate upload success with more detailed feedback
    const fileNames = files.map(f => f.name).join(', ');
    alert(`✅ Successfully uploaded ${files.length} file(s): ${fileNames}\n\n🤖 AI analysis has been initiated and will be available in ~2 minutes.\n\n📧 You'll receive a notification when processing is complete.`);
  };

  const handleContractSelect = (contract: any) => {
    console.log('Contract selected:', contract);
    // Simulate opening contract details with more context
    alert(`📄 Opening Contract Details\n\n` +
          `Contract: ${contract.name}\n` +
          `Status: ${contract.status}\n` +
          `Risk Level: ${contract.riskLevel.toUpperCase()}\n` +
          `AI Confidence: ${contract.aiConfidence}%\n` +
          `Issues Found: ${contract.issues}\n` +
          `Assigned to: ${contract.assignee}\n\n` +
          `⚡ Quick Actions Available:\n` +
          `• Review redlines (${contract.redlines})\n` +
          `• Send for approval\n` +
          `• Export to PDF\n` +
          `• Schedule meeting`);
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardContent onUpload={handleUpload} onContractSelect={handleContractSelect} searchQuery={searchQuery} />;
      case 'contracts':
        return <ContractsContent onContractSelect={handleContractSelect} searchQuery={searchQuery} />;
      case 'gdpr':
        return <GDPRContent />;
      case 'uk-legal':
        return <UKLegalContent />;
      case 'queue':
        return <ReviewQueueContent onContractSelect={handleContractSelect} searchQuery={searchQuery} />;
      case 'insights':
        return <AIInsightsContent />;
      default:
        return <DashboardContent onUpload={handleUpload} onContractSelect={handleContractSelect} searchQuery={searchQuery} />;
    }
  };

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      // This would normally handle closing dropdowns, but for demo purposes we'll keep it simple
    };
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black flex overflow-hidden">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="flex-1 flex flex-col">
        <Header activeTab={activeTab} />
        
        <main className="flex-1 p-8 overflow-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}
