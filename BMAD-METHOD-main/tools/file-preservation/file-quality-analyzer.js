const fs = require('node:fs');
const fsPromises = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const { createReadStream } = require('node:fs');
const { pipeline } = require('node:stream/promises');

// Minimal chalk replacement for basic colors
const chalk = {
  red: (text) => `\x1b[31m${text}\x1b[0m`,
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
  cyan: (text) => `\x1b[36m${text}\x1b[0m`,
  white: (text) => text,
  dim: (text) => `\x1b[2m${text}\x1b[0m`
};

/**
 * Enhanced file quality analyzer for intelligent file preservation
 * Provides comprehensive file assessment to identify "good files" worth preserving
 */
class FileQualityAnalyzer {
  constructor(options = {}) {
    this.options = {
      minFileSize: options.minFileSize || 1, // Minimum file size in bytes
      maxFileSize: options.maxFileSize || 100 * 1024 * 1024, // 100MB default max
      textExtensions: options.textExtensions || ['.md', '.txt', '.js', '.ts', '.py', '.yaml', '.yml', '.json'],
      codeExtensions: options.codeExtensions || ['.js', '.ts', '.py', '.java', '.cpp', '.c', '.h', '.go', '.rs'],
      docExtensions: options.docExtensions || ['.md', '.txt', '.pdf', '.docx', '.doc'],
      configExtensions: options.configExtensions || ['.yaml', '.yml', '.json', '.toml', '.ini', '.conf'],
      ignorePatterns: options.ignorePatterns || [
        'node_modules/**',
        '.git/**',
        '**/*.log',
        '**/tmp/**',
        '**/temp/**',
        '**/.DS_Store',
        '**/thumbs.db'
      ],
      ...options
    };
  }

  /**
   * Helper function to ensure directory exists (fs-extra replacement)
   */
  async ensureDir(dirPath) {
    try {
      await fsPromises.mkdir(dirPath, { recursive: true });
    } catch (error) {
      if (error.code !== 'EEXIST') {
        throw error;
      }
    }
  }

  /**
   * Analyze a single file for quality metrics
   * @param {string} filePath - Absolute path to the file
   * @returns {Promise<Object>} File quality assessment
   */
  async analyzeFile(filePath) {
    try {
      const stats = await fsPromises.stat(filePath);
      const relativePath = path.relative(process.cwd(), filePath);
      const extension = path.extname(filePath).toLowerCase();
      const basename = path.basename(filePath);
      
      const analysis = {
        path: relativePath,
        absolutePath: filePath,
        name: basename,
        extension,
        size: stats.size,
        modifiedTime: stats.mtime,
        createdTime: stats.birthtime,
        isDirectory: stats.isDirectory(),
        isFile: stats.isFile(),
        qualityScore: 0,
        qualityFactors: {},
        recommendations: [],
        hash: null,
        contentType: this.determineContentType(extension),
        metadata: {}
      };

      if (!analysis.isFile) {
        return analysis;
      }

      // Calculate quality factors
      await this.assessSizeQuality(analysis);
      await this.assessNameQuality(analysis);
      await this.assessExtensionQuality(analysis);
      await this.assessContentQuality(analysis);
      await this.assessAgeQuality(analysis);
      await this.calculateFileHash(analysis);

      // Calculate overall quality score (0-100)
      analysis.qualityScore = this.calculateOverallScore(analysis.qualityFactors);
      
      // Generate preservation recommendations
      analysis.recommendations = this.generateRecommendations(analysis);

      return analysis;
    } catch (error) {
      return {
        path: path.relative(process.cwd(), filePath),
        absolutePath: filePath,
        error: error.message,
        qualityScore: 0,
        recommendations: ['ERROR: Unable to analyze file']
      };
    }
  }

  /**
   * Determine content type based on file extension
   */
  determineContentType(extension) {
    if (this.options.codeExtensions.includes(extension)) return 'code';
    if (this.options.docExtensions.includes(extension)) return 'documentation';
    if (this.options.configExtensions.includes(extension)) return 'configuration';
    if (['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'].includes(extension)) return 'image';
    if (['.mp4', '.avi', '.mkv', '.mov'].includes(extension)) return 'video';
    if (['.mp3', '.wav', '.flac', '.ogg'].includes(extension)) return 'audio';
    if (['.zip', '.tar', '.gz', '.rar', '.7z'].includes(extension)) return 'archive';
    if (['.exe', '.dll', '.so', '.dylib'].includes(extension)) return 'binary';
    return 'other';
  }

  /**
   * Assess file size quality
   */
  async assessSizeQuality(analysis) {
    const { size } = analysis;
    let score = 50; // Base score
    const factors = {};

    if (size === 0) {
      score = 0;
      factors.emptyFile = true;
    } else if (size < 10) {
      score = 20;
      factors.tooSmall = true;
    } else if (size > this.options.maxFileSize) {
      score = 30;
      factors.tooLarge = true;
    } else if (size >= 1024 && size <= 10 * 1024 * 1024) {
      score = 80; // Good size range
      factors.goodSize = true;
    }

    analysis.qualityFactors.size = { score, factors };
  }

  /**
   * Assess filename quality
   */
  async assessNameQuality(analysis) {
    const { name } = analysis;
    let score = 50;
    const factors = {};

    // Check for meaningful names
    if (name.length < 3) {
      score -= 20;
      factors.tooShort = true;
    }

    // Check for common junk patterns
    const junkPatterns = [
      /^temp/i, /^tmp/i, /^test/i, /^debug/i, /^backup/i,
      /copy/i, /untitled/i, /new\s*file/i, /\d{8,}/
    ];
    
    if (junkPatterns.some(pattern => pattern.test(name))) {
      score -= 30;
      factors.junkName = true;
    }

    // Bonus for descriptive names
    if (name.length > 10 && /[a-zA-Z]/.test(name)) {
      score += 10;
      factors.descriptive = true;
    }

    // Check for version numbers or dates (often valuable)
    if (/v\d+|version|_\d{4}[-_]\d{2}[-_]\d{2}/.test(name)) {
      score += 15;
      factors.versioned = true;
    }

    analysis.qualityFactors.name = { score: Math.max(0, Math.min(100, score)), factors };
  }

  /**
   * Assess file extension quality
   */
  async assessExtensionQuality(analysis) {
    const { extension, contentType } = analysis;
    let score = 50;
    const factors = {};

    // High-value content types
    const highValueTypes = ['code', 'documentation', 'configuration'];
    if (highValueTypes.includes(contentType)) {
      score += 30;
      factors.highValueType = true;
    }

    // Low-value or problematic extensions
    const lowValueExtensions = ['.tmp', '.bak', '.old', '.cache', '.log'];
    if (lowValueExtensions.includes(extension)) {
      score -= 40;
      factors.lowValueExtension = true;
    }

    // No extension penalty
    if (!extension) {
      score -= 10;
      factors.noExtension = true;
    }

    analysis.qualityFactors.extension = { score: Math.max(0, Math.min(100, score)), factors };
  }

  /**
   * Assess content quality for text files
   */
  async assessContentQuality(analysis) {
    const { absolutePath, extension, size } = analysis;
    let score = 50;
    const factors = {};

    // Only analyze text files under 1MB to avoid performance issues
    if (!this.options.textExtensions.includes(extension) || size > 1024 * 1024) {
      analysis.qualityFactors.content = { score, factors: { notAnalyzed: true } };
      return;
    }

    try {
      const content = await fsPromises.readFile(absolutePath, 'utf-8');
      analysis.metadata.lineCount = content.split('\n').length;
      analysis.metadata.charCount = content.length;
      analysis.metadata.wordCount = content.split(/\s+/).filter(word => word.length > 0).length;

      // Content quality indicators
      if (analysis.metadata.lineCount > 10) {
        score += 20;
        factors.substantialContent = true;
      }

      // Check for meaningful content patterns
      const meaningfulPatterns = [
        /function\s+\w+/g, // Function definitions
        /class\s+\w+/g,   // Class definitions
        /import\s+/g,     // Import statements
        /##\s+/g,         // Markdown headers
        /TODO|FIXME|NOTE/gi, // Development notes
        /https?:\/\//g    // URLs
      ];

      const patternMatches = meaningfulPatterns.reduce((count, pattern) => {
        const matches = content.match(pattern);
        return count + (matches ? matches.length : 0);
      }, 0);

      if (patternMatches > 5) {
        score += 25;
        factors.richContent = true;
      }

      // Check for duplicated content (repeated lines)
      const lines = content.split('\n');
      const uniqueLines = new Set(lines.filter(line => line.trim().length > 0));
      const duplicateRatio = 1 - (uniqueLines.size / lines.length);
      
      if (duplicateRatio > 0.7) {
        score -= 30;
        factors.highDuplication = true;
      }

      analysis.metadata.duplicateRatio = duplicateRatio;
      analysis.metadata.patternMatches = patternMatches;

    } catch (error) {
      factors.contentReadError = true;
      score -= 10;
    }

    analysis.qualityFactors.content = { score: Math.max(0, Math.min(100, score)), factors };
  }

  /**
   * Assess age-based quality
   */
  async assessAgeQuality(analysis) {
    const { modifiedTime } = analysis;
    let score = 50;
    const factors = {};

    const now = new Date();
    const daysSinceModified = (now - modifiedTime) / (1000 * 60 * 60 * 24);

    if (daysSinceModified < 7) {
      score += 20;
      factors.recentlyModified = true;
    } else if (daysSinceModified < 30) {
      score += 10;
      factors.recentlyActive = true;
    } else if (daysSinceModified > 365) {
      score -= 15;
      factors.stale = true;
    }

    analysis.qualityFactors.age = { score: Math.max(0, Math.min(100, score)), factors };
  }

  /**
   * Calculate file hash for deduplication
   */
  async calculateFileHash(analysis) {
    try {
      const hash = crypto.createHash('sha256');
      const stream = createReadStream(analysis.absolutePath);
      
      for await (const chunk of stream) {
        hash.update(chunk);
      }
      
      analysis.hash = hash.digest('hex');
    } catch (error) {
      analysis.hash = null;
    }
  }

  /**
   * Calculate overall quality score
   */
  calculateOverallScore(qualityFactors) {
    const weights = {
      size: 0.2,
      name: 0.15,
      extension: 0.2,
      content: 0.3,
      age: 0.15
    };

    let totalScore = 0;
    let totalWeight = 0;

    for (const [factor, weight] of Object.entries(weights)) {
      if (qualityFactors[factor]) {
        totalScore += qualityFactors[factor].score * weight;
        totalWeight += weight;
      }
    }

    return totalWeight > 0 ? Math.round(totalScore / totalWeight) : 0;
  }

  /**
   * Generate preservation recommendations
   */
  generateRecommendations(analysis) {
    const recommendations = [];
    const { qualityScore, qualityFactors, contentType } = analysis;

    if (qualityScore >= 80) {
      recommendations.push('HIGH_PRIORITY: Definitely preserve this file');
    } else if (qualityScore >= 60) {
      recommendations.push('MEDIUM_PRIORITY: Consider preserving with review');
    } else if (qualityScore >= 40) {
      recommendations.push('LOW_PRIORITY: Preserve only if space permits');
    } else {
      recommendations.push('SKIP: Consider not preserving this file');
    }

    // Specific recommendations based on factors
    if (qualityFactors.size?.factors.emptyFile) {
      recommendations.push('WARNING: Empty file - safe to delete');
    }

    if (qualityFactors.size?.factors.tooLarge) {
      recommendations.push('LARGE_FILE: Review if this large file is necessary');
    }

    if (qualityFactors.name?.factors.junkName) {
      recommendations.push('POOR_NAME: File has generic/temporary name');
    }

    if (qualityFactors.content?.factors.richContent) {
      recommendations.push('RICH_CONTENT: File contains valuable code/documentation patterns');
    }

    if (qualityFactors.age?.factors.stale) {
      recommendations.push('STALE: File hasn\'t been modified in over a year');
    }

    if (['code', 'documentation', 'configuration'].includes(contentType)) {
      recommendations.push('VALUABLE_TYPE: This file type is typically important to preserve');
    }

    return recommendations;
  }

  /**
   * Analyze multiple files in a directory
   * @param {string} dirPath - Directory to analyze
   * @param {Object} options - Analysis options
   * @returns {Promise<Array>} Array of file analyses
   */
  async analyzeDirectory(dirPath, options = {}) {
    const { recursive = true, includeHidden = false } = options;
    const results = [];

    try {
      const entries = await fsPromises.readdir(dirPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        
        // Skip hidden files unless requested
        if (!includeHidden && entry.name.startsWith('.')) {
          continue;
        }

        // Skip ignored patterns
        const relativePath = path.relative(process.cwd(), fullPath);
        if (this.shouldIgnore(relativePath)) {
          continue;
        }

        if (entry.isFile()) {
          const analysis = await this.analyzeFile(fullPath);
          results.push(analysis);
        } else if (entry.isDirectory() && recursive) {
          const subResults = await this.analyzeDirectory(fullPath, options);
          results.push(...subResults);
        }
      }
    } catch (error) {
      console.error(chalk.red(`Error analyzing directory ${dirPath}:`), error.message);
    }

    return results;
  }

  /**
   * Check if a file should be ignored based on patterns
   */
  shouldIgnore(filePath) {
    // Simple pattern matching without micromatch dependency
    for (const pattern of this.options.ignorePatterns) {
      if (pattern.includes('**')) {
        const simplePattern = pattern.replace('**/', '').replace('/**', '');
        if (filePath.includes(simplePattern)) {
          return true;
        }
      } else if (filePath.includes(pattern.replace('*', ''))) {
        return true;
      }
    }
    return false;
  }

  /**
   * Generate a comprehensive quality report
   */
  generateQualityReport(analyses) {
    const report = {
      totalFiles: analyses.length,
      averageScore: 0,
      scoreDistribution: { high: 0, medium: 0, low: 0, poor: 0 },
      contentTypes: {},
      recommendations: {
        preserve: [],
        review: [],
        skip: []
      },
      duplicates: [],
      summary: {}
    };

    // Calculate statistics
    let totalScore = 0;
    const hashGroups = new Map();

    for (const analysis of analyses) {
      if (analysis.error) continue;

      totalScore += analysis.qualityScore;

      // Score distribution
      if (analysis.qualityScore >= 80) report.scoreDistribution.high++;
      else if (analysis.qualityScore >= 60) report.scoreDistribution.medium++;
      else if (analysis.qualityScore >= 40) report.scoreDistribution.low++;
      else report.scoreDistribution.poor++;

      // Content type distribution
      const contentType = analysis.contentType || 'unknown';
      report.contentTypes[contentType] = (report.contentTypes[contentType] || 0) + 1;

      // Group by hash for duplicate detection
      if (analysis.hash) {
        if (!hashGroups.has(analysis.hash)) {
          hashGroups.set(analysis.hash, []);
        }
        hashGroups.get(analysis.hash).push(analysis);
      }

      // Categorize recommendations
      const hasHighPriority = analysis.recommendations.some(r => r.includes('HIGH_PRIORITY'));
      const hasMediumPriority = analysis.recommendations.some(r => r.includes('MEDIUM_PRIORITY'));
      const hasSkip = analysis.recommendations.some(r => r.includes('SKIP'));

      if (hasHighPriority) {
        report.recommendations.preserve.push(analysis);
      } else if (hasMediumPriority) {
        report.recommendations.review.push(analysis);
      } else if (hasSkip) {
        report.recommendations.skip.push(analysis);
      }
    }

    report.averageScore = Math.round(totalScore / Math.max(1, analyses.length - analyses.filter(a => a.error).length));

    // Find duplicates
    for (const [hash, files] of hashGroups.entries()) {
      if (files.length > 1) {
        // Sort by quality score to identify the best version
        files.sort((a, b) => b.qualityScore - a.qualityScore);
        report.duplicates.push({
          hash,
          files,
          bestFile: files[0],
          duplicateCount: files.length - 1
        });
      }
    }

    report.summary = {
      totalSize: analyses.reduce((sum, a) => sum + (a.size || 0), 0),
      preserveCount: report.recommendations.preserve.length,
      reviewCount: report.recommendations.review.length,
      skipCount: report.recommendations.skip.length,
      duplicateGroups: report.duplicates.length,
      duplicateFiles: report.duplicates.reduce((sum, d) => sum + d.duplicateCount, 0)
    };

    return report;
  }
}

module.exports = FileQualityAnalyzer;