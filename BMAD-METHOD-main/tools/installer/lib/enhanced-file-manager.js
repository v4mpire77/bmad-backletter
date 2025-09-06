const fs = require('fs-extra');
const path = require('node:path');
const crypto = require('node:crypto');
const yaml = require('js-yaml');
const chalk = require('chalk');
const { createReadStream, createWriteStream, promises: fsPromises } = require('node:fs');
const { pipeline } = require('node:stream/promises');
const resourceLocator = require('./resource-locator');
const SmartFilePreservationManager = require('../../file-preservation/smart-preservation-manager');

/**
 * Enhanced File Manager with Smart Preservation capabilities
 * Extends the existing BMAD file manager with intelligent file handling
 */
class EnhancedFileManager {
  constructor() {
    this.preservationManager = null;
    this.preservationEnabled = false;
  }

  /**
   * Enable smart preservation features
   */
  enableSmartPreservation(options = {}) {
    this.preservationManager = new SmartFilePreservationManager({
      preservationMode: options.mode || 'intelligent',
      minQualityThreshold: options.threshold || 40,
      preservationRoot: options.preservationRoot || './preserved-files',
      analysisRoot: options.analysisRoot || './file-analysis',
      ...options
    });
    this.preservationEnabled = true;
    console.log(chalk.green('✅ Smart preservation enabled'));
  }

  /**
   * Enhanced copy file with preservation analysis
   */
  async copyFileWithPreservation(source, destination, options = {}) {
    try {
      // Analyze file quality if preservation is enabled
      if (this.preservationEnabled && options.analyzeQuality) {
        const analysis = await this.preservationManager.analyzer.analyzeFile(source);
        
        if (analysis.qualityScore < (options.minQuality || 20)) {
          console.log(chalk.yellow(`⚠️  Low quality file detected: ${source} (score: ${analysis.qualityScore})`));
          
          if (options.skipLowQuality) {
            console.log(chalk.dim(`⏭️  Skipping low quality file`));
            return false;
          }
        }

        // Log quality information if verbose
        if (options.verbose) {
          console.log(chalk.dim(`📊 Quality score for ${path.basename(source)}: ${analysis.qualityScore}/100`));
        }
      }

      // Use existing copy logic
      await fs.ensureDir(path.dirname(destination));

      // Use streaming for large files (> 10MB)
      const stats = await fs.stat(source);
      await (stats.size > 10 * 1024 * 1024
        ? pipeline(createReadStream(source), createWriteStream(destination))
        : fs.copy(source, destination));
      
      return true;
    } catch (error) {
      console.error(chalk.red(`Failed to copy ${source}:`), error.message);
      return false;
    }
  }

  /**
   * Enhanced directory copy with smart preservation
   */
  async copyDirectoryWithSmartPreservation(source, destination, options = {}) {
    try {
      console.log(chalk.blue(`📁 Smart copying directory: ${source} → ${destination}`));
      
      if (this.preservationEnabled) {
        // Analyze the entire directory first
        console.log(chalk.yellow('🔍 Analyzing directory for quality...'));
        const analyses = await this.preservationManager.analyzer.analyzeDirectory(source, {
          recursive: true,
          includeHidden: options.includeHidden || false
        });

        const report = this.preservationManager.analyzer.generateQualityReport(analyses);
        console.log(chalk.green(`📊 Analyzed ${analyses.length} files, avg quality: ${report.averageScore}/100`));

        // Copy files based on quality
        let copiedCount = 0;
        let skippedCount = 0;

        for (const analysis of analyses) {
          if (analysis.error) continue;

          const sourcePath = analysis.absolutePath;
          const relativePath = path.relative(source, sourcePath);
          const destinationPath = path.join(destination, relativePath);

          const shouldCopy = this.shouldCopyFile(analysis, options);
          
          if (shouldCopy.copy) {
            const success = await this.copyFileWithPreservation(sourcePath, destinationPath, {
              ...options,
              analyzeQuality: false // Already analyzed
            });
            
            if (success) {
              copiedCount++;
              if (options.verbose) {
                console.log(chalk.green(`✅ Copied: ${relativePath} (${shouldCopy.reason})`));
              }
            }
          } else {
            skippedCount++;
            if (options.verbose) {
              console.log(chalk.yellow(`⏭️  Skipped: ${relativePath} (${shouldCopy.reason})`));
            }
          }
        }

        console.log(chalk.blue(`📁 Copy completed: ${copiedCount} copied, ${skippedCount} skipped`));
        return true;

      } else {
        // Fallback to regular directory copy
        return await this.copyDirectory(source, destination);
      }

    } catch (error) {
      console.error(chalk.red(`Failed to copy directory ${source}:`), error.message);
      return false;
    }
  }

  /**
   * Determine if a file should be copied based on quality analysis
   */
  shouldCopyFile(analysis, options = {}) {
    const { qualityScore, recommendations, contentType } = analysis;
    const minQuality = options.minQuality || 20;
    const mode = options.preservationMode || 'intelligent';

    // Always copy high-priority files
    if (recommendations.some(r => r.includes('HIGH_PRIORITY'))) {
      return { copy: true, reason: 'High priority file' };
    }

    // Skip empty files unless explicitly requested
    if (qualityScore === 0 && !options.includeEmptyFiles) {
      return { copy: false, reason: 'Empty file' };
    }

    // Apply quality threshold
    if (qualityScore < minQuality) {
      return { copy: false, reason: `Quality ${qualityScore} below threshold ${minQuality}` };
    }

    // Mode-specific logic
    switch (mode) {
      case 'conservative':
        if (qualityScore >= 60 || ['code', 'documentation', 'configuration'].includes(contentType)) {
          return { copy: true, reason: 'Conservative mode: acceptable quality' };
        }
        return { copy: false, reason: 'Conservative mode: quality too low' };

      case 'aggressive':
        return { copy: true, reason: 'Aggressive mode: copy everything above threshold' };

      case 'intelligent':
      default:
        if (qualityScore >= 40) {
          return { copy: true, reason: 'Intelligent mode: good quality' };
        }
        if (['code', 'documentation', 'configuration'].includes(contentType) && qualityScore >= 30) {
          return { copy: true, reason: 'Intelligent mode: important content type' };
        }
        return { copy: false, reason: 'Intelligent mode: low quality' };
    }
  }

  /**
   * Create a backup with smart analysis
   */
  async createSmartBackup(sourcePath, backupPath, options = {}) {
    console.log(chalk.blue(`🛡️  Creating smart backup: ${sourcePath} → ${backupPath}`));

    if (this.preservationEnabled) {
      // Create backup strategy
      const strategy = await this.preservationManager.createBackupStrategy(sourcePath, {
        ...options,
        outputPath: backupPath
      });

      // Execute backup based on strategy
      await fs.ensureDir(backupPath);
      
      let backedUpCount = 0;
      const allFiles = [...strategy.backupPlan.immediate, ...strategy.backupPlan.scheduled];
      
      for (const filePath of allFiles) {
        const sourceFile = path.join(sourcePath, filePath);
        const backupFile = path.join(backupPath, filePath);
        
        try {
          await fs.ensureDir(path.dirname(backupFile));
          await fs.copy(sourceFile, backupFile, { preserveTimestamps: true });
          backedUpCount++;
        } catch (error) {
          console.error(chalk.red(`Failed to backup ${filePath}:`), error.message);
        }
      }

      console.log(chalk.green(`✅ Smart backup completed: ${backedUpCount} files backed up`));
      return true;

    } else {
      // Fallback to regular backup
      await fs.copy(sourcePath, backupPath, { preserveTimestamps: true });
      console.log(chalk.green(`✅ Regular backup completed`));
      return true;
    }
  }

  /**
   * Migrate documents with preservation
   */
  async migrateDocumentsWithPreservation(sourcePath, destinationPath, options = {}) {
    console.log(chalk.blue(`📚 Migrating documents with smart preservation...`));

    if (!this.preservationEnabled) {
      console.log(chalk.yellow('⚠️  Smart preservation not enabled, using standard migration'));
      return await this.migrateDocuments(sourcePath, destinationPath, options);
    }

    try {
      // Analyze documents first
      const analyses = await this.preservationManager.analyzer.analyzeDirectory(sourcePath, {
        recursive: true
      });

      // Filter for document files
      const documentAnalyses = analyses.filter(a => 
        ['documentation', 'configuration'].includes(a.contentType) ||
        a.extension.match(/\.(md|txt|pdf|docx|doc|yaml|yml|json)$/i)
      );

      console.log(chalk.green(`📊 Found ${documentAnalyses.length} document files`));

      // Preserve high-quality documents
      const preservedDocs = [];
      const skippedDocs = [];

      for (const analysis of documentAnalyses) {
        const shouldPreserve = this.preservationManager.shouldPreserveFile(analysis, options);
        
        if (shouldPreserve.preserve) {
          const relativePath = path.relative(sourcePath, analysis.absolutePath);
          const destPath = path.join(destinationPath, relativePath);
          
          await fs.ensureDir(path.dirname(destPath));
          await fs.copy(analysis.absolutePath, destPath, { preserveTimestamps: true });
          
          preservedDocs.push({
            path: relativePath,
            qualityScore: analysis.qualityScore,
            reason: shouldPreserve.reason
          });
        } else {
          skippedDocs.push({
            path: path.relative(sourcePath, analysis.absolutePath),
            qualityScore: analysis.qualityScore,
            reason: shouldPreserve.reason
          });
        }
      }

      console.log(chalk.green(`✅ Document migration completed:`));
      console.log(chalk.white(`  📄 Preserved: ${preservedDocs.length} documents`));
      console.log(chalk.yellow(`  ⏭️  Skipped: ${skippedDocs.length} documents`));

      // Save migration report
      const migrationReport = {
        timestamp: new Date().toISOString(),
        sourcePath,
        destinationPath,
        preservedDocs,
        skippedDocs,
        summary: {
          totalAnalyzed: documentAnalyses.length,
          preserved: preservedDocs.length,
          skipped: skippedDocs.length
        }
      };

      const reportPath = path.join(destinationPath, 'migration-report.json');
      await fs.writeJson(reportPath, migrationReport, { spaces: 2 });
      console.log(chalk.dim(`📋 Migration report saved to: ${reportPath}`));

      return true;

    } catch (error) {
      console.error(chalk.red('❌ Document migration failed:'), error.message);
      return false;
    }
  }

  // Include all original FileManager methods
  async copyFile(source, destination) {
    try {
      await fs.ensureDir(path.dirname(destination));

      // Use streaming for large files (> 10MB)
      const stats = await fs.stat(source);
      await (stats.size > 10 * 1024 * 1024
        ? pipeline(createReadStream(source), createWriteStream(destination))
        : fs.copy(source, destination));
      return true;
    } catch (error) {
      console.error(chalk.red(`Failed to copy ${source}:`), error.message);
      return false;
    }
  }

  async copyDirectory(source, destination) {
    try {
      await fs.ensureDir(destination);

      // Use streaming copy for large directories
      const files = await resourceLocator.findFiles('**/*', {
        cwd: source,
        nodir: true,
      });

      // Process files in batches to avoid memory issues
      const batchSize = 50;
      for (let index = 0; index < files.length; index += batchSize) {
        const batch = files.slice(index, index + batchSize);
        await Promise.all(
          batch.map((file) => this.copyFile(path.join(source, file), path.join(destination, file))),
        );
      }
      return true;
    } catch (error) {
      console.error(chalk.red(`Failed to copy directory ${source}:`), error.message);
      return false;
    }
  }

  async copyFileWithRootReplacement(source, destination, rootValue) {
    try {
      // Check file size to determine if we should stream
      const stats = await fs.stat(source);

      if (stats.size > 5 * 1024 * 1024) {
        // 5MB threshold
        // Use streaming for large files
        const { Transform } = require('node:stream');
        const replaceStream = new Transform({
          transform(chunk, encoding, callback) {
            const modified = chunk.toString().replaceAll('{root}', rootValue);
            callback(null, modified);
          },
        });

        await this.ensureDirectory(path.dirname(destination));
        await pipeline(
          createReadStream(source, { encoding: 'utf8' }),
          replaceStream,
          createWriteStream(destination, { encoding: 'utf8' }),
        );
      } else {
        // Regular approach for smaller files
        const content = await fsPromises.readFile(source, 'utf8');
        const updatedContent = content.replaceAll('{root}', rootValue);
        await this.ensureDirectory(path.dirname(destination));
        await fsPromises.writeFile(destination, updatedContent, 'utf8');
      }

      return true;
    } catch (error) {
      console.error(chalk.red(`Failed to copy ${source} with root replacement:`), error.message);
      return false;
    }
  }

  async copyDirectoryWithRootReplacement(
    source,
    destination,
    rootValue,
    fileExtensions = ['.md', '.yaml', '.yml'],
  ) {
    try {
      await this.ensureDirectory(destination);

      // Get all files in source directory
      const files = await resourceLocator.findFiles('**/*', {
        cwd: source,
        nodir: true,
      });

      let replacedCount = 0;

      for (const file of files) {
        const sourcePath = path.join(source, file);
        const destinationPath = path.join(destination, file);

        // Check if this file type should have {root} replacement
        const shouldReplace = fileExtensions.some((extension) => file.endsWith(extension));

        if (shouldReplace) {
          if (await this.copyFileWithRootReplacement(sourcePath, destinationPath, rootValue)) {
            replacedCount++;
          }
        } else {
          // Regular copy for files that don't need replacement
          await this.copyFile(sourcePath, destinationPath);
        }
      }

      if (replacedCount > 0) {
        console.log(chalk.dim(`  Processed ${replacedCount} files with {root} replacement`));
      }

      return true;
    } catch (error) {
      console.error(
        chalk.red(`Failed to copy directory ${source} with root replacement:`),
        error.message,
      );
      return false;
    }
  }

  async copyGlobPattern(pattern, sourceDir, destDir, rootValue = null) {
    const files = await resourceLocator.findFiles(pattern, { cwd: sourceDir });
    const copied = [];

    for (const file of files) {
      const sourcePath = path.join(sourceDir, file);
      const destinationPath = path.join(destDir, file);

      // Use root replacement if rootValue is provided and file needs it
      const needsRootReplacement =
        rootValue && (file.endsWith('.md') || file.endsWith('.yaml') || file.endsWith('.yml'));

      let success = false;
      success = await (needsRootReplacement
        ? this.copyFileWithRootReplacement(sourcePath, destinationPath, rootValue)
        : this.copyFile(sourcePath, destinationPath));

      if (success) {
        copied.push(file);
      }
    }

    return copied;
  }

  async ensureDirectory(dirPath) {
    try {
      await fs.ensureDir(dirPath);
      return true;
    } catch (error) {
      console.error(chalk.red(`Failed to create directory ${dirPath}:`), error.message);
      return false;
    }
  }

  async pathExists(checkPath) {
    try {
      await fs.access(checkPath);
      return true;
    } catch {
      return false;
    }
  }

  async calculateFileHash(filePath) {
    try {
      // Use streaming for hash calculation to reduce memory usage
      const stream = createReadStream(filePath);
      const hash = crypto.createHash('sha256');

      for await (const chunk of stream) {
        hash.update(chunk);
      }

      return hash.digest('hex').slice(0, 16);
    } catch {
      return null;
    }
  }

  async checkFileIntegrity(installDir, manifest) {
    const result = {
      missing: [],
      modified: [],
    };

    for (const file of manifest.files) {
      const filePath = path.join(installDir, file.path);

      // Skip checking the manifest file itself - it will always be different due to timestamps
      if (file.path.endsWith('install-manifest.yaml')) {
        continue;
      }

      if (await this.pathExists(filePath)) {
        const currentHash = await this.calculateFileHash(filePath);
        if (currentHash && currentHash !== file.hash) {
          result.modified.push(file.path);
        }
      } else {
        result.missing.push(file.path);
      }
    }

    return result;
  }

  async checkModifiedFiles(installDir, manifest) {
    const modified = [];

    for (const file of manifest.files) {
      const filePath = path.join(installDir, file.path);
      const currentHash = await this.calculateFileHash(filePath);

      if (currentHash && currentHash !== file.hash) {
        modified.push(file.path);
      }
    }

    return modified;
  }

  manifestDir = '.bmad-core';
  manifestFile = 'install-manifest.yaml';
}

module.exports = new EnhancedFileManager();