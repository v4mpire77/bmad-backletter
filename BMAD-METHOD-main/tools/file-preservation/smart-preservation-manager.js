const fs = require('fs-extra');
const path = require('node:path');
const chalk = require('chalk');
const FileQualityAnalyzer = require('./file-quality-analyzer');

/**
 * Smart File Preservation Manager
 * Provides intelligent file backup, migration, and preservation strategies
 * Based on quality analysis and smart deduplication
 */
class SmartFilePreservationManager {
  constructor(options = {}) {
    this.options = {
      preservationMode: options.preservationMode || 'intelligent', // 'intelligent', 'conservative', 'aggressive'
      minQualityThreshold: options.minQualityThreshold || 40,
      deduplicate: options.deduplicate !== false, // Default to true
      createBackups: options.createBackups !== false, // Default to true
      backupSuffix: options.backupSuffix || '.backup',
      preservationRoot: options.preservationRoot || './preserved',
      analysisRoot: options.analysisRoot || './analysis',
      ...options
    };

    this.analyzer = new FileQualityAnalyzer(options.analyzerOptions);
    this.preservationLog = [];
  }

  /**
   * Main preservation workflow
   * @param {string} sourcePath - Source directory to preserve from
   * @param {Object} options - Preservation options
   * @returns {Promise<Object>} Preservation result summary
   */
  async preserveFiles(sourcePath, options = {}) {
    const startTime = Date.now();
    console.log(chalk.blue(`\n🔍 Starting smart file preservation from: ${sourcePath}`));

    try {
      // Step 1: Analyze all files
      console.log(chalk.yellow('📊 Analyzing file quality...'));
      const analyses = await this.analyzer.analyzeDirectory(sourcePath, {
        recursive: true,
        includeHidden: options.includeHidden || false
      });

      if (analyses.length === 0) {
        console.log(chalk.yellow('⚠️  No files found to analyze'));
        return { success: false, reason: 'No files found' };
      }

      console.log(chalk.green(`✅ Analyzed ${analyses.length} files`));

      // Step 2: Generate quality report
      const report = this.analyzer.generateQualityReport(analyses);
      await this.saveAnalysisReport(report, analyses);

      // Step 3: Execute preservation strategy
      console.log(chalk.yellow('💾 Executing preservation strategy...'));
      const preservationResult = await this.executePreservationStrategy(analyses, report, options);

      // Step 4: Generate final summary
      const summary = {
        success: true,
        executionTime: Date.now() - startTime,
        sourcePath,
        totalFilesAnalyzed: analyses.length,
        filesPreserved: preservationResult.preserved.length,
        filesSkipped: preservationResult.skipped.length,
        duplicatesResolved: preservationResult.duplicatesResolved.length,
        spaceSaved: preservationResult.spaceSaved,
        qualityReport: report,
        preservationLog: this.preservationLog
      };

      await this.saveSummaryReport(summary);
      this.displaySummary(summary);

      return summary;
    } catch (error) {
      console.error(chalk.red('❌ Preservation failed:'), error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * Execute the preservation strategy based on mode and quality analysis
   */
  async executePreservationStrategy(analyses, report, options) {
    const result = {
      preserved: [],
      skipped: [],
      duplicatesResolved: [],
      spaceSaved: 0
    };

    // Handle duplicates first
    if (this.options.deduplicate && report.duplicates.length > 0) {
      console.log(chalk.cyan(`🔄 Processing ${report.duplicates.length} duplicate groups...`));
      const deduplicationResult = await this.handleDuplicates(report.duplicates);
      result.duplicatesResolved = deduplicationResult.resolved;
      result.spaceSaved += deduplicationResult.spaceSaved;
    }

    // Preserve files based on strategy
    const filesToProcess = analyses.filter(a => !a.error);
    console.log(chalk.cyan(`📁 Processing ${filesToProcess.length} files for preservation...`));

    for (const analysis of filesToProcess) {
      const shouldPreserve = this.shouldPreserveFile(analysis, options);
      
      if (shouldPreserve.preserve) {
        try {
          await this.preserveFile(analysis, shouldPreserve.reason);
          result.preserved.push({
            path: analysis.path,
            reason: shouldPreserve.reason,
            qualityScore: analysis.qualityScore,
            preservedTo: this.getPreservationPath(analysis)
          });
        } catch (error) {
          console.error(chalk.red(`Failed to preserve ${analysis.path}:`), error.message);
          this.logAction('ERROR', analysis.path, `Failed to preserve: ${error.message}`);
        }
      } else {
        result.skipped.push({
          path: analysis.path,
          reason: shouldPreserve.reason,
          qualityScore: analysis.qualityScore
        });
        this.logAction('SKIP', analysis.path, shouldPreserve.reason);
      }
    }

    return result;
  }

  /**
   * Determine if a file should be preserved based on strategy and quality
   */
  shouldPreserveFile(analysis, options) {
    const { qualityScore, recommendations, contentType } = analysis;
    const mode = options.preservationMode || this.options.preservationMode;

    // Always preserve high-priority files
    if (recommendations.some(r => r.includes('HIGH_PRIORITY'))) {
      return { preserve: true, reason: 'High quality score and priority' };
    }

    // Handle different preservation modes
    switch (mode) {
      case 'conservative':
        // Only preserve very high quality files
        if (qualityScore >= 80) {
          return { preserve: true, reason: 'Conservative mode: High quality file' };
        }
        if (['code', 'documentation', 'configuration'].includes(contentType) && qualityScore >= 70) {
          return { preserve: true, reason: 'Conservative mode: Important file type with good quality' };
        }
        return { preserve: false, reason: 'Conservative mode: Quality below threshold' };

      case 'aggressive':
        // Preserve most files except obvious junk
        if (qualityScore >= 20) {
          return { preserve: true, reason: 'Aggressive mode: Above minimum threshold' };
        }
        if (recommendations.some(r => r.includes('WARNING: Empty file'))) {
          return { preserve: false, reason: 'Aggressive mode: Empty file' };
        }
        return { preserve: true, reason: 'Aggressive mode: Default preserve' };

      case 'intelligent':
      default:
        // Intelligent decision based on multiple factors
        if (qualityScore >= this.options.minQualityThreshold) {
          return { preserve: true, reason: `Intelligent mode: Quality score ${qualityScore} above threshold` };
        }
        
        // Special handling for important content types
        if (['code', 'documentation', 'configuration'].includes(contentType)) {
          if (qualityScore >= 30) {
            return { preserve: true, reason: 'Intelligent mode: Important content type' };
          }
        }

        // Check for specific valuable indicators
        if (analysis.metadata?.patternMatches > 0) {
          return { preserve: true, reason: 'Intelligent mode: Contains valuable patterns' };
        }

        return { preserve: false, reason: `Intelligent mode: Quality score ${qualityScore} below threshold` };
    }
  }

  /**
   * Handle duplicate files by preserving the best version
   */
  async handleDuplicates(duplicateGroups) {
    const result = {
      resolved: [],
      spaceSaved: 0
    };

    for (const group of duplicateGroups) {
      const { bestFile, files } = group;
      const duplicates = files.filter(f => f.path !== bestFile.path);

      // Preserve the best file
      await this.preserveFile(bestFile, `Best version of ${files.length} duplicates`);

      // Calculate space saved from duplicates
      const duplicateSpace = duplicates.reduce((sum, file) => sum + file.size, 0);
      result.spaceSaved += duplicateSpace;

      result.resolved.push({
        hash: group.hash,
        preservedFile: bestFile.path,
        duplicateFiles: duplicates.map(f => f.path),
        spaceSaved: duplicateSpace
      });

      this.logAction('DEDUP', bestFile.path, `Preserved best of ${files.length} duplicates`);
      duplicates.forEach(dup => {
        this.logAction('DEDUP_SKIP', dup.path, `Duplicate of ${bestFile.path}`);
      });
    }

    return result;
  }

  /**
   * Preserve a single file to the preservation directory
   */
  async preserveFile(analysis, reason) {
    const destinationPath = this.getPreservationPath(analysis);
    
    // Ensure destination directory exists
    await fs.ensureDir(path.dirname(destinationPath));

    // Copy the file with metadata preservation
    await fs.copy(analysis.absolutePath, destinationPath, {
      preserveTimestamps: true,
      errorOnExist: false,
      overwrite: true
    });

    // Save analysis metadata alongside the file
    const metadataPath = destinationPath + '.analysis.json';
    await fs.writeJson(metadataPath, {
      originalPath: analysis.path,
      preservationDate: new Date().toISOString(),
      reason,
      qualityScore: analysis.qualityScore,
      recommendations: analysis.recommendations,
      metadata: analysis.metadata
    }, { spaces: 2 });

    this.logAction('PRESERVE', analysis.path, reason);
  }

  /**
   * Get the preservation path for a file
   */
  getPreservationPath(analysis) {
    // Organize by content type and quality
    const contentType = analysis.contentType || 'other';
    const qualityTier = analysis.qualityScore >= 80 ? 'high-quality' :
                       analysis.qualityScore >= 60 ? 'medium-quality' :
                       analysis.qualityScore >= 40 ? 'low-quality' : 'poor-quality';
    
    const basePath = path.join(this.options.preservationRoot, contentType, qualityTier);
    return path.join(basePath, analysis.path);
  }

  /**
   * Save analysis report to disk
   */
  async saveAnalysisReport(report, analyses) {
    await fs.ensureDir(this.options.analysisRoot);
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const reportPath = path.join(this.options.analysisRoot, `quality-report-${timestamp}.json`);
    const detailedPath = path.join(this.options.analysisRoot, `detailed-analysis-${timestamp}.json`);

    await fs.writeJson(reportPath, report, { spaces: 2 });
    await fs.writeJson(detailedPath, analyses, { spaces: 2 });

    console.log(chalk.dim(`📋 Analysis report saved to: ${reportPath}`));
  }

  /**
   * Save preservation summary report
   */
  async saveSummaryReport(summary) {
    await fs.ensureDir(this.options.analysisRoot);
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const summaryPath = path.join(this.options.analysisRoot, `preservation-summary-${timestamp}.json`);

    await fs.writeJson(summaryPath, summary, { spaces: 2 });
    console.log(chalk.dim(`📋 Preservation summary saved to: ${summaryPath}`));
  }

  /**
   * Log preservation actions
   */
  logAction(action, filePath, reason) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      action,
      file: filePath,
      reason
    };
    this.preservationLog.push(logEntry);
  }

  /**
   * Display preservation summary
   */
  displaySummary(summary) {
    console.log(chalk.blue('\n📊 PRESERVATION SUMMARY'));
    console.log(chalk.blue('='.repeat(50)));
    
    console.log(chalk.white(`📁 Source: ${summary.sourcePath}`));
    console.log(chalk.white(`⏱️  Execution time: ${(summary.executionTime / 1000).toFixed(2)}s`));
    console.log(chalk.white(`📊 Files analyzed: ${summary.totalFilesAnalyzed}`));
    console.log(chalk.green(`✅ Files preserved: ${summary.filesPreserved}`));
    console.log(chalk.yellow(`⏭️  Files skipped: ${summary.filesSkipped}`));
    console.log(chalk.cyan(`🔄 Duplicates resolved: ${summary.duplicatesResolved.length}`));
    
    if (summary.spaceSaved > 0) {
      console.log(chalk.magenta(`💾 Space saved: ${this.formatBytes(summary.spaceSaved)}`));
    }

    // Quality distribution
    const { scoreDistribution } = summary.qualityReport;
    console.log(chalk.blue('\n📈 Quality Distribution:'));
    console.log(chalk.green(`  High (80-100): ${scoreDistribution.high} files`));
    console.log(chalk.yellow(`  Medium (60-79): ${scoreDistribution.medium} files`));
    console.log(chalk.orange(`  Low (40-59): ${scoreDistribution.low} files`));
    console.log(chalk.red(`  Poor (0-39): ${scoreDistribution.poor} files`));

    // Content type distribution
    console.log(chalk.blue('\n📂 Content Types:'));
    for (const [type, count] of Object.entries(summary.qualityReport.contentTypes)) {
      console.log(chalk.white(`  ${type}: ${count} files`));
    }

    console.log(chalk.blue('\n' + '='.repeat(50)));
  }

  /**
   * Format bytes for human readable display
   */
  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  /**
   * Create a backup strategy for critical files
   */
  async createBackupStrategy(sourcePath, options = {}) {
    console.log(chalk.blue('\n🛡️  Creating backup strategy...'));

    const analyses = await this.analyzer.analyzeDirectory(sourcePath);
    const criticalFiles = analyses.filter(a => 
      a.qualityScore >= 80 || 
      ['code', 'documentation', 'configuration'].includes(a.contentType)
    );

    const strategy = {
      timestamp: new Date().toISOString(),
      sourcePath,
      totalFiles: analyses.length,
      criticalFiles: criticalFiles.length,
      backupPlan: {
        immediate: [], // Files to backup immediately
        scheduled: [], // Files for regular backup
        versioned: []  // Files needing version control
      }
    };

    // Categorize files for backup strategy
    for (const file of criticalFiles) {
      if (file.qualityScore >= 90 || file.recommendations.some(r => r.includes('HIGH_PRIORITY'))) {
        strategy.backupPlan.immediate.push(file.path);
      } else if (file.qualityFactors.age?.factors.recentlyModified) {
        strategy.backupPlan.scheduled.push(file.path);
      } else {
        strategy.backupPlan.versioned.push(file.path);
      }
    }

    // Save strategy
    const strategyPath = path.join(this.options.analysisRoot, 'backup-strategy.json');
    await fs.writeJson(strategyPath, strategy, { spaces: 2 });

    console.log(chalk.green(`✅ Backup strategy created: ${criticalFiles.length} critical files identified`));
    console.log(chalk.yellow(`⚡ Immediate backup: ${strategy.backupPlan.immediate.length} files`));
    console.log(chalk.cyan(`📅 Scheduled backup: ${strategy.backupPlan.scheduled.length} files`));
    console.log(chalk.blue(`📚 Versioned backup: ${strategy.backupPlan.versioned.length} files`));

    return strategy;
  }
}

module.exports = SmartFilePreservationManager;