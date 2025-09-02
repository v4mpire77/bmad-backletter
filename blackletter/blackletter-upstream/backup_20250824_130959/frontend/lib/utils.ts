/**
 * Blackletter GDPR Processor - Utility Functions
 * Context Engineering Framework v2.0.0 Compliant
 */
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { format, formatDistanceToNow, parseISO } from "date-fns";

/**
 * Utility function for combining Tailwind classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format file size in human readable format
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Format percentage with proper precision
 */
export function formatPercentage(value: number, precision: number = 1): string {
  return `${(value * 100).toFixed(precision)}%`;
}

/**
 * Format confidence score as percentage
 */
export function formatConfidence(confidence: number): string {
  return formatPercentage(confidence, 0);
}

/**
 * Format processing time in human readable format
 */
export function formatProcessingTime(seconds: number): string {
  if (seconds < 1) {
    return `${Math.round(seconds * 1000)}ms`;
  } else if (seconds < 60) {
    return `${seconds.toFixed(1)}s`;
  } else {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.round(seconds % 60);
    return `${minutes}m ${remainingSeconds}s`;
  }
}

/**
 * Format timestamp for display
 */
export function formatTimestamp(timestamp: string | Date): string {
  try {
    const date = typeof timestamp === 'string' ? parseISO(timestamp) : timestamp;
    return format(date, 'MMM dd, yyyy HH:mm:ss');
  } catch (error) {
    console.error('Error formatting timestamp:', error);
    return 'Invalid date';
  }
}

/**
 * Format relative time (e.g., "2 minutes ago")
 */
export function formatRelativeTime(timestamp: string | Date): string {
  try {
    const date = typeof timestamp === 'string' ? parseISO(timestamp) : timestamp;
    return formatDistanceToNow(date, { addSuffix: true });
  } catch (error) {
    console.error('Error formatting relative time:', error);
    return 'Unknown time';
  }
}

/**
 * Truncate text with ellipsis
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

/**
 * Generate a random ID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

/**
 * Validate file type
 */
export function isValidFileType(file: File, allowedTypes: string[]): boolean {
  const fileExtension = file.name.split('.').pop()?.toLowerCase();
  return fileExtension ? allowedTypes.includes(fileExtension) : false;
}

/**
 * Validate file size
 */
export function isValidFileSize(file: File, maxSizeBytes: number): boolean {
  return file.size <= maxSizeBytes;
}

/**
 * Sleep utility for async operations
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Debounce function calls
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

/**
 * Copy text to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
}

/**
 * Download data as file
 */
export function downloadAsFile(data: string, filename: string, mimeType: string = 'text/plain'): void {
  const blob = new Blob([data], { type: mimeType });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Convert issues to CSV format
 */
export function convertIssuesToCSV(issues: any[]): string {
  if (issues.length === 0) return '';
  
  const headers = ['ID', 'Article', 'Severity', 'Confidence', 'Status', 'Snippet', 'Recommendation'];
  const csvRows = [headers.join(',')];
  
  for (const issue of issues) {
    const row = [
      issue.id,
      issue.citation,
      issue.severity,
      formatConfidence(issue.confidence),
      issue.status,
      `"${issue.snippet.replace(/"/g, '""')}"`, // Escape quotes
      `"${issue.recommendation.replace(/"/g, '""')}"`
    ];
    csvRows.push(row.join(','));
  }
  
  return csvRows.join('\n');
}

/**
 * Convert coverage to CSV format
 */
export function convertCoverageToCSV(coverage: any[]): string {
  if (coverage.length === 0) return '';
  
  const headers = ['Article', 'Status', 'Confidence', 'Present', 'Strength'];
  const csvRows = [headers.join(',')];
  
  for (const item of coverage) {
    const row = [
      item.article,
      item.status,
      formatConfidence(item.confidence),
      item.present ? 'Yes' : 'No',
      item.strength
    ];
    csvRows.push(row.join(','));
  }
  
  return csvRows.join('\n');
}

/**
 * Local storage utilities
 */
export const storage = {
  get: <T>(key: string, defaultValue: T): T => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  },
  
  set: <T>(key: string, value: T): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Failed to save to localStorage:', error);
    }
  },
  
  remove: (key: string): void => {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Failed to remove from localStorage:', error);
    }
  }
};

/**
 * Theme utilities
 */
export const theme = {
  toggle: (): void => {
    const root = document.documentElement;
    const isDark = root.classList.contains('dark');
    
    if (isDark) {
      root.classList.remove('dark');
      storage.set('theme', 'light');
    } else {
      root.classList.add('dark');
      storage.set('theme', 'dark');
    }
  },
  
  init: (): void => {
    const savedTheme = storage.get('theme', 'light');
    const root = document.documentElement;
    
    if (savedTheme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }
};