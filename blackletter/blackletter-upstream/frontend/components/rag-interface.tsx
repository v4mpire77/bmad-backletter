"use client";

import React, { useState, useRef, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { 
  Upload, 
  Search, 
  FileText, 
  Brain, 
  BarChart3, 
  Loader2, 
  CheckCircle, 
  AlertCircle,
  X
} from 'lucide-react';

/**
 * Document interface for RAG system documents
 */
interface Document {
  doc_id: string;
  filename: string;
  upload_time: string;
  size: number;
  chunks_created: number;
  status: 'processing' | 'completed' | 'error';
}

/**
 * Query result interface for RAG responses
 */
interface QueryResult {
  answer: string;
  chunks: Array<{
    id: string;
    text: string;
    page: number;
    similarity_score: number;
    start_pos: number;
    end_pos: number;
  }>;
  query: string;
  total_chunks_retrieved: number;
}

/**
 * Search result interface for document chunks
 */
interface SearchResult {
  id: string;
  doc_id: string;
  text: string;
  page: number;
  similarity_score: number;
  start_pos: number;
  end_pos: number;
  metadata: Record<string, unknown>;
}

/**
 * Error state interface
 */
interface ErrorState {
  message: string;
  type: 'error' | 'warning' | 'info';
}

/**
 * Props interface for RAG Interface component
 */
interface RAGInterfaceProps {
  /** Optional callback for document upload completion */
  onUploadComplete?: (document: Document) => void;
  /** Optional callback for query completion */
  onQueryComplete?: (result: QueryResult) => void;
  /** Optional custom styling classes */
  className?: string;
  /** Accessibility label for screen readers */
  'aria-label'?: string;
}

/**
 * RAG Interface Component
 * 
 * Provides a comprehensive interface for document upload, querying, and search
 * functionality using the RAG (Retrieval-Augmented Generation) system.
 * 
 * Features:
 * - Document upload with progress tracking
 * - Semantic search and querying
 * - Results visualization
 * - Accessibility compliant (WCAG 2.1 AA)
 * - Responsive design
 */
export const RAGInterface: React.FC<RAGInterfaceProps> = ({
  onUploadComplete,
  onQueryComplete,
  className = '',
  'aria-label': ariaLabel = 'RAG Document Analysis Interface'
}) => {
  // State management
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<string>('');
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<ErrorState | null>(null);
  const [activeTab, setActiveTab] = useState('upload');
  
  // Refs
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Constants
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
  const ACCEPTED_FILE_TYPES = ['.pdf', '.doc', '.docx', '.txt'];

  // Helper functions
  const clearError = useCallback(() => setError(null), []);
  
  const setErrorState = useCallback((message: string, type: ErrorState['type'] = 'error') => {
    setError({ message, type });
  }, []);

  const formatFileSize = useCallback((bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }, []);

  const validateFile = useCallback((file: File): boolean => {
    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      setErrorState(`File size exceeds maximum limit of ${formatFileSize(MAX_FILE_SIZE)}`);
      return false;
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!ACCEPTED_FILE_TYPES.includes(fileExtension || '')) {
      setErrorState(`File type not supported. Accepted formats: ${ACCEPTED_FILE_TYPES.join(', ')}`);
      return false;
    }

    return true;
  }, [formatFileSize, setErrorState]);

  // Upload document with enhanced error handling and progress tracking
  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    clearError();

    // Validate file
    if (!validateFile(file)) {
      return;
    }

    setIsLoading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Create XMLHttpRequest for progress tracking
      const xhr = new XMLHttpRequest();
      
      const uploadPromise = new Promise<Document>((resolve, reject) => {
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            setUploadProgress(percentComplete);
          }
        });

        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const result = JSON.parse(xhr.responseText);
              resolve(result);
            } catch (e) {
              reject(new Error('Invalid response format'));
            }
          } else {
            reject(new Error(xhr.responseText || 'Upload failed'));
          }
        });

        xhr.addEventListener('error', () => {
          reject(new Error('Network error during upload'));
        });

        xhr.open('POST', `${API_BASE}/api/rag/upload`);
        xhr.send(formData);
      });

      const result = await uploadPromise;
      
      setDocuments(prev => [...prev, result]);
      setUploadProgress(100);
      setErrorState('Document uploaded successfully!', 'info');
      
      // Call callback if provided
      onUploadComplete?.(result);
      
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

    } catch (error) {
      setErrorState(
        error instanceof Error ? error.message : 'Upload failed. Please try again.',
        'error'
      );
    } finally {
      setIsLoading(false);
      // Reset progress after a delay to show completion
      setTimeout(() => setUploadProgress(0), 2000);
    }
  }, [API_BASE, clearError, validateFile, onUploadComplete, setErrorState]);

  // Query documents with enhanced error handling
  const handleQuery = useCallback(async () => {
    if (!query.trim()) {
      setErrorState('Please enter a query', 'warning');
      return;
    }

    clearError();
    setIsLoading(true);
    setQueryResult(null);

    try {
      const formData = new URLSearchParams({
        query: query.trim(),
        top_k: '5',
        use_semantic_search: 'true'
      });

      if (selectedDocument) {
        formData.append('doc_id', selectedDocument);
      }

      const response = await fetch(`${API_BASE}/api/rag/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setQueryResult(result);
        setErrorState('Query completed successfully', 'info');
        
        // Call callback if provided
        onQueryComplete?.(result);
      } else {
        const errorText = await response.text();
        setErrorState(`Query failed: ${errorText}`, 'error');
      }
    } catch (error) {
      setErrorState(
        error instanceof Error ? error.message : 'Query failed. Please try again.',
        'error'
      );
    } finally {
      setIsLoading(false);
    }
  }, [query, selectedDocument, API_BASE, clearError, setErrorState, onQueryComplete]);

  // Search documents
  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const formData = new URLSearchParams({
        query: query,
        top_k: '10',
        similarity_threshold: '0.7'
      });

      if (selectedDocument) {
        formData.append('doc_id', selectedDocument);
      }

      const response = await fetch(`${API_BASE}/api/rag/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setSearchResults(result.results || []);
      } else {
        const error = await response.text();
        alert(`Search failed: ${error}`);
      }
    } catch (error) {
      alert(`Search error: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Load documents
  const loadDocuments = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/rag/documents`);
      if (response.ok) {
        const result = await response.json();
        setDocuments(result.documents || []);
      }
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  };

  // Load documents on component mount
  React.useEffect(() => {
    loadDocuments();
  }, []);

  return (
    <div 
      className={`w-full max-w-7xl mx-auto p-6 space-y-6 ${className}`}
      aria-label={ariaLabel}
      role="main"
    >
      {/* Header Section - Following Design System */}
      <div className="text-center space-y-4 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 leading-tight">
          RAG Document Analysis
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload legal documents and query them using advanced retrieval-augmented generation 
          for intelligent contract analysis and compliance checking.
        </p>
      </div>

      {/* Error/Success Alert */}
      {error && (
        <Alert 
          className={`mb-6 ${
            error.type === 'error' ? 'border-red-200 bg-red-50' :
            error.type === 'warning' ? 'border-yellow-200 bg-yellow-50' :
            'border-blue-200 bg-blue-50'
          }`}
        >
          {error.type === 'error' ? (
            <AlertCircle className="h-4 w-4 text-red-600" />
          ) : error.type === 'warning' ? (
            <AlertCircle className="h-4 w-4 text-yellow-600" />
          ) : (
            <CheckCircle className="h-4 w-4 text-blue-600" />
          )}
          <AlertDescription className={
            error.type === 'error' ? 'text-red-700' :
            error.type === 'warning' ? 'text-yellow-700' :
            'text-blue-700'
          }>
            {error.message}
          </AlertDescription>
          <Button
            variant="ghost"
            size="sm"
            onClick={clearError}
            className="ml-auto h-6 w-6 p-0"
            aria-label="Close alert"
          >
            <X className="h-4 w-4" />
          </Button>
        </Alert>
      )}

      {/* Main Interface Tabs */}
      <Tabs 
        value={activeTab} 
        onValueChange={setActiveTab}
        className="w-full"
      >
        <TabsList className="grid w-full grid-cols-4 bg-gray-100 p-1 rounded-lg">
          <TabsTrigger 
            value="upload" 
            className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:text-blue-600 data-[state=active]:shadow-sm"
          >
            <Upload className="h-4 w-4" />
            Upload
          </TabsTrigger>
          <TabsTrigger 
            value="query" 
            className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:text-blue-600 data-[state=active]:shadow-sm"
          >
            <Brain className="h-4 w-4" />
            Query
          </TabsTrigger>
          <TabsTrigger 
            value="search" 
            className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:text-blue-600 data-[state=active]:shadow-sm"
          >
            <Search className="h-4 w-4" />
            Search
          </TabsTrigger>
          <TabsTrigger 
            value="documents" 
            className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:text-blue-600 data-[state=active]:shadow-sm"
          >
            <FileText className="h-4 w-4" />
            Documents
          </TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="space-y-6">
          <Card className="shadow-sm border-gray-200">
            <CardHeader className="bg-gray-50 border-b border-gray-200">
              <CardTitle className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                <Upload className="h-5 w-5 text-blue-600" />
                Upload Document
              </CardTitle>
              <CardDescription className="text-gray-600">
                Upload legal documents (PDF, DOCX, TXT) for AI-powered analysis and compliance checking.
                Maximum file size: {formatFileSize(MAX_FILE_SIZE)}.
              </CardDescription>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
              {/* File Upload Area */}
              <div className="border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors rounded-lg p-8 text-center bg-gray-50 hover:bg-blue-50">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept={ACCEPTED_FILE_TYPES.join(',')}
                  onChange={handleFileUpload}
                  className="hidden"
                  aria-label="Upload document file"
                  aria-describedby="file-upload-description"
                  disabled={isLoading}
                />
                <div className="space-y-4">
                  <div className="p-3 bg-blue-100 rounded-full w-fit mx-auto">
                    <Upload className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="space-y-2">
                    <Button
                      onClick={() => fileInputRef.current?.click()}
                      disabled={isLoading}
                      variant="default"
                      size="lg"
                      className="bg-blue-600 hover:bg-blue-700 text-white"
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Processing...
                        </>
                      ) : (
                        <>
                          <Upload className="h-4 w-4 mr-2" />
                          Choose File
                        </>
                      )}
                    </Button>
                    <p id="file-upload-description" className="text-sm text-gray-500">
                      or drag and drop • Supported: {ACCEPTED_FILE_TYPES.join(', ')} • Max: {formatFileSize(MAX_FILE_SIZE)}
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Upload Progress */}
              {uploadProgress > 0 && (
                <div className="space-y-3">
                  <div className="flex justify-between items-center text-sm">
                    <span className="font-medium text-gray-700">Upload Progress</span>
                    <span className="text-blue-600 font-semibold">{Math.round(uploadProgress)}%</span>
                  </div>
                  <Progress 
                    value={uploadProgress} 
                    className="w-full h-2"
                    aria-label={`Upload progress: ${Math.round(uploadProgress)}%`}
                  />
                </div>
              )}

              {/* Upload Instructions */}
              {!isLoading && uploadProgress === 0 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="text-sm font-semibold text-blue-900 mb-2">Upload Guidelines:</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• Ensure documents are clearly readable and properly formatted</li>
                    <li>• Legal contracts and agreements work best with this system</li>
                    <li>• Processing time depends on document length and complexity</li>
                    <li>• Uploaded documents are securely processed and stored</li>
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="query" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Query Documents</CardTitle>
              <CardDescription>
                Ask questions about your documents and get AI-powered answers
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Select Document (Optional)</label>
                <select
                  value={selectedDocument}
                  onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSelectedDocument(e.target.value)}
                  className="w-full p-2 border rounded-md"
                  aria-label="Select document to query"
                >
                  <option value="">All Documents</option>
                  {documents.map((doc) => (
                    <option key={doc.doc_id} value={doc.doc_id}>
                      {doc.filename}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Your Question</label>
                <Textarea
                  value={query}
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setQuery(e.target.value)}
                  placeholder="e.g., What are the payment terms in this contract?"
                  rows={3}
                />
              </div>

              <Button onClick={handleQuery} disabled={isLoading || !query.trim()}>
                {isLoading ? 'Processing...' : 'Ask Question'}
              </Button>

              {queryResult && (
                <div className="space-y-4 mt-6">
                  <Separator />
                  <div>
                    <h3 className="font-semibold mb-2">Answer:</h3>
                    <p className="text-sm bg-gray-50 p-3 rounded-md">
                      {queryResult.answer}
                    </p>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2">Sources ({queryResult.total_chunks_retrieved}):</h3>
                    <div className="space-y-2">
                      {queryResult.chunks.map((chunk, index) => (
                        <div key={chunk.id} className="text-sm bg-gray-50 p-3 rounded-md">
                          <div className="flex justify-between items-center mb-1">
                            <Badge variant="secondary">Page {chunk.page}</Badge>
                            <Badge variant="outline">
                              Score: {chunk.similarity_score}
                            </Badge>
                          </div>
                          <p className="text-xs text-muted-foreground">
                            {chunk.text}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="search" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Search Documents</CardTitle>
              <CardDescription>
                Find specific content across your documents
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Select Document (Optional)</label>
                <select
                  value={selectedDocument}
                  onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSelectedDocument(e.target.value)}
                  className="w-full p-2 border rounded-md"
                  aria-label="Select document to search"
                >
                  <option value="">All Documents</option>
                  {documents.map((doc) => (
                    <option key={doc.doc_id} value={doc.doc_id}>
                      {doc.filename}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Search Query</label>
                <Input
                  value={query}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.target.value)}
                  placeholder="e.g., liability clause, payment terms"
                />
              </div>

              <Button onClick={handleSearch} disabled={isLoading || !query.trim()}>
                {isLoading ? 'Searching...' : 'Search'}
              </Button>

              {searchResults.length > 0 && (
                <div className="space-y-4 mt-6">
                  <Separator />
                  <h3 className="font-semibold">Search Results ({searchResults.length}):</h3>
                  <div className="space-y-2">
                    {searchResults.map((result, index) => (
                      <div key={result.id} className="text-sm bg-gray-50 p-3 rounded-md">
                        <div className="flex justify-between items-center mb-1">
                          <Badge variant="secondary">Page {result.page}</Badge>
                          <Badge variant="outline">
                            Score: {result.similarity_score}
                          </Badge>
                        </div>
                        <p className="text-xs text-muted-foreground mb-1">
                          Document: {result.doc_id}
                        </p>
                        <p className="text-xs">
                          {result.text}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="documents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Document Library</CardTitle>
              <CardDescription>
                Manage your uploaded documents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {documents.length === 0 ? (
                  <p className="text-center text-muted-foreground">
                    No documents uploaded yet. Upload a document to get started.
                  </p>
                ) : (
                  documents.map((doc) => (
                    <div key={doc.doc_id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="space-y-1">
                        <h3 className="font-medium">{doc.filename}</h3>
                        <p className="text-sm text-muted-foreground">
                          Uploaded: {new Date(doc.upload_time).toLocaleDateString()}
                        </p>
                        <div className="flex gap-2">
                          <Badge variant="outline">
                            {doc.chunks_created} chunks
                          </Badge>
                          <Badge variant="secondary">
                            {(doc.size / 1024 / 1024).toFixed(2)} MB
                          </Badge>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setSelectedDocument(doc.doc_id)}
                        >
                          Select
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
