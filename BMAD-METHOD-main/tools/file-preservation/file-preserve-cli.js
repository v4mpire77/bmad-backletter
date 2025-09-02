#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('node:path');
const chalk = require('chalk');
const SmartFilePreservationManager = require('./smart-preservation-manager');
const FileQualityAnalyzer = require('./file-quality-analyzer');

/**
 * CLI tool for smart file preservation
 * Enhanced version of the BMAD file management tools
 */
class FilePreservationCLI {
  constructor() {
    this.commands = {
      analyze: this.analyzeCommand.bind(this),
      preserve: this.preserveCommand.bind(this),
      backup: this.backupCommand.bind(this),
      'clean-dupes': this.cleanDupesCommand.bind(this),
      report: this.reportCommand.bind(this),
      help: this.helpCommand.bind(this)
    };
  }

  async run() {
    const args = process.argv.slice(2);
    const command = args[0];
    const options = this.parseArgs(args.slice(1));

    if (!command || !this.commands[command]) {
      this.helpCommand();
      return;
    }

    try {
      await this.commands[command](options);
    } catch (error) {
      console.error(chalk.red('❌ Command failed:'), error.message);
      if (options.verbose) {
        console.error(error.stack);
      }
      process.exit(1);
    }
  }

  parseArgs(args) {
    const options = {};
    for (let i = 0; i < args.length; i++) {
      const arg = args[i];
      if (arg.startsWith('--')) {
        const key = arg.slice(2);
        const nextArg = args[i + 1];
        if (nextArg && !nextArg.startsWith('--')) {
          options[key] = nextArg;
          i++; // Skip next arg since we used it as value
        } else {
          options[key] = true;
        }
      } else if (!options.source) {
        options.source = arg;
      }
    }
    return options;
  }

  async analyzeCommand(options) {
    const sourcePath = options.source || '.';
    console.log(chalk.blue(`🔍 Analyzing files in: ${sourcePath}`));

    const analyzer = new FileQualityAnalyzer({
      ignorePatterns: options['ignore-patterns'] ? options['ignore-patterns'].split(',') : undefined
    });

    const analyses = await analyzer.analyzeDirectory(sourcePath, {
      recursive: options.recursive !== false,
      includeHidden: options['include-hidden'] || false
    });

    const report = analyzer.generateQualityReport(analyses);

    // Display summary
    console.log(chalk.blue('\n📊 ANALYSIS SUMMARY'));
    console.log(chalk.blue('='.repeat(40)));
    console.log(chalk.white(`📁 Files analyzed: ${report.totalFiles}`));
    console.log(chalk.white(`📈 Average quality: ${report.averageScore}/100`));
    
    console.log(chalk.blue('\n📈 Quality Distribution:'));
    console.log(chalk.green(`  High (80-100): ${report.scoreDistribution.high} files`));
    console.log(chalk.yellow(`  Medium (60-79): ${report.scoreDistribution.medium} files`));
    console.log(chalk.orange(`  Low (40-59): ${report.scoreDistribution.low} files`));
    console.log(chalk.red(`  Poor (0-39): ${report.scoreDistribution.poor} files`));

    console.log(chalk.blue('\n📂 Content Types:'));
    for (const [type, count] of Object.entries(report.contentTypes)) {
      console.log(chalk.white(`  ${type}: ${count} files`));
    }

    if (report.duplicates.length > 0) {
      console.log(chalk.cyan(`\n🔄 Found ${report.duplicates.length} duplicate groups`));
      console.log(chalk.cyan(`💾 Potential space savings: ${this.formatBytes(
        report.duplicates.reduce((sum, d) => sum + (d.duplicateCount * d.files[0].size), 0)
      )}`));
    }

    // Save detailed report if requested
    if (options.output) {
      await fs.writeJson(options.output, { report, analyses }, { spaces: 2 });
      console.log(chalk.green(`\n📋 Detailed report saved to: ${options.output}`));
    }

    // Show top recommendations
    this.showTopRecommendations(report);
  }

  async preserveCommand(options) {
    const sourcePath = options.source || '.';
    const preservationMode = options.mode || 'intelligent';
    
    console.log(chalk.blue(`💾 Preserving files from: ${sourcePath}`));
    console.log(chalk.yellow(`🎯 Mode: ${preservationMode}`));

    const manager = new SmartFilePreservationManager({
      preservationMode,
      minQualityThreshold: parseInt(options.threshold) || 40,
      deduplicate: options.dedupe !== false,
      preservationRoot: options.dest || './preserved',
      analysisRoot: options['analysis-dir'] || './analysis'
    });

    const result = await manager.preserveFiles(sourcePath, {
      includeHidden: options['include-hidden'] || false,
      preservationMode
    });

    if (result.success) {
      console.log(chalk.green('\n✅ Preservation completed successfully!'));
    } else {
      console.log(chalk.red('\n❌ Preservation failed:'), result.reason || result.error);
    }
  }

  async backupCommand(options) {
    const sourcePath = options.source || '.';
    
    console.log(chalk.blue(`🛡️  Creating backup strategy for: ${sourcePath}`));

    const manager = new SmartFilePreservationManager({
      analysisRoot: options['analysis-dir'] || './analysis'
    });

    const strategy = await manager.createBackupStrategy(sourcePath, options);
    
    if (options.execute) {
      console.log(chalk.yellow('⚡ Executing immediate backups...'));
      // Execute immediate backups
      for (const filePath of strategy.backupPlan.immediate) {
        const backupPath = path.join(options.dest || './backups', filePath + '.backup');
        await fs.ensureDir(path.dirname(backupPath));
        await fs.copy(path.join(sourcePath, filePath), backupPath, { preserveTimestamps: true });
        console.log(chalk.green(`✅ Backed up: ${filePath}`));
      }
    }
  }

  async cleanDupesCommand(options) {
    const sourcePath = options.source || '.';
    
    console.log(chalk.blue(`🔄 Finding and cleaning duplicates in: ${sourcePath}`));

    const analyzer = new FileQualityAnalyzer();
    const analyses = await analyzer.analyzeDirectory(sourcePath, {
      recursive: options.recursive !== false
    });

    const report = analyzer.generateQualityReport(analyses);
    
    if (report.duplicates.length === 0) {
      console.log(chalk.green('✅ No duplicates found!'));
      return;
    }

    console.log(chalk.yellow(`🔍 Found ${report.duplicates.length} duplicate groups`));

    for (const group of report.duplicates) {
      console.log(chalk.cyan(`\n📂 Duplicate group (${group.files.length} files):`));
      console.log(chalk.green(`  ✅ Keep: ${group.bestFile.path} (score: ${group.bestFile.qualityScore})`));
      
      for (const duplicate of group.files.slice(1)) {
        console.log(chalk.red(`  ❌ Remove: ${duplicate.path} (score: ${duplicate.qualityScore})`));
        
        if (options.execute && !options['dry-run']) {
          try {
            await fs.remove(duplicate.absolutePath);
            console.log(chalk.dim(`    🗑️  Deleted`));
          } catch (error) {
            console.log(chalk.red(`    ❌ Failed to delete: ${error.message}`));
          }
        }
      }
    }

    const spaceSaved = report.duplicates.reduce((sum, d) => 
      sum + (d.duplicateCount * d.files[0].size), 0
    );

    console.log(chalk.blue(`\n💾 Space that would be saved: ${this.formatBytes(spaceSaved)}`));
    
    if (!options.execute) {
      console.log(chalk.yellow('🔍 This was a dry run. Use --execute to actually delete duplicates.'));
    }
  }

  async reportCommand(options) {
    const analysisDir = options['analysis-dir'] || './analysis';
    
    try {
      const files = await fs.readdir(analysisDir);
      const reportFiles = files.filter(f => f.startsWith('preservation-summary-') && f.endsWith('.json'));
      
      if (reportFiles.length === 0) {
        console.log(chalk.yellow('📭 No preservation reports found'));
        return;
      }

      // Get latest report
      const latestReport = reportFiles.sort().reverse()[0];
      const reportPath = path.join(analysisDir, latestReport);
      const report = await fs.readJson(reportPath);

      console.log(chalk.blue('\n📊 LATEST PRESERVATION REPORT'));
      console.log(chalk.blue('='.repeat(50)));
      
      console.log(chalk.white(`📅 Date: ${new Date(report.qualityReport?.timestamp || Date.now()).toLocaleString()}`));
      console.log(chalk.white(`📁 Source: ${report.sourcePath}`));
      console.log(chalk.white(`⏱️  Duration: ${(report.executionTime / 1000).toFixed(2)}s`));
      console.log(chalk.green(`✅ Files preserved: ${report.filesPreserved}`));
      console.log(chalk.yellow(`⏭️  Files skipped: ${report.filesSkipped}`));
      
      if (report.spaceSaved > 0) {
        console.log(chalk.magenta(`💾 Space saved: ${this.formatBytes(report.spaceSaved)}`));
      }

      // Show preservation log summary
      if (report.preservationLog && options.verbose) {
        console.log(chalk.blue('\n📋 Action Summary:'));
        const actions = {};
        for (const entry of report.preservationLog) {
          actions[entry.action] = (actions[entry.action] || 0) + 1;
        }
        for (const [action, count] of Object.entries(actions)) {
          console.log(chalk.white(`  ${action}: ${count}`));
        }
      }

    } catch (error) {
      console.log(chalk.red('❌ Failed to read reports:'), error.message);
    }
  }

  helpCommand() {
    console.log(chalk.blue('\n🔧 Smart File Preservation Tool'));
    console.log(chalk.blue('='.repeat(40)));
    console.log(chalk.white('Enhanced file management for the BMAD Method'));
    
    console.log(chalk.yellow('\nCommands:'));
    console.log(chalk.white('  analyze <path>     - Analyze file quality in directory'));
    console.log(chalk.white('  preserve <path>    - Smart file preservation'));
    console.log(chalk.white('  backup <path>      - Create backup strategy'));
    console.log(chalk.white('  clean-dupes <path> - Find and remove duplicates'));
    console.log(chalk.white('  report             - Show latest preservation report'));
    console.log(chalk.white('  help               - Show this help'));

    console.log(chalk.yellow('\nCommon Options:'));
    console.log(chalk.white('  --source <path>      Source directory (default: current)'));
    console.log(chalk.white('  --dest <path>        Destination directory'));
    console.log(chalk.white('  --mode <mode>        Preservation mode (intelligent|conservative|aggressive)'));
    console.log(chalk.white('  --threshold <num>    Quality threshold (0-100)'));
    console.log(chalk.white('  --include-hidden     Include hidden files'));
    console.log(chalk.white('  --execute            Execute actions (vs dry-run)'));
    console.log(chalk.white('  --verbose            Verbose output'));
    console.log(chalk.white('  --output <file>      Save detailed report to file'));

    console.log(chalk.yellow('\nExamples:'));
    console.log(chalk.dim('  file-preserve analyze ./my-project --output report.json'));
    console.log(chalk.dim('  file-preserve preserve ./legacy-code --mode conservative --dest ./preserved'));
    console.log(chalk.dim('  file-preserve clean-dupes ./documents --execute'));
    console.log(chalk.dim('  file-preserve backup ./critical-files --execute --dest ./backups'));
  }

  showTopRecommendations(report) {
    console.log(chalk.blue('\n🏆 TOP RECOMMENDATIONS'));
    console.log(chalk.blue('-'.repeat(30)));

    // Show top files to preserve
    const topPreserve = report.recommendations.preserve
      .sort((a, b) => b.qualityScore - a.qualityScore)
      .slice(0, 5);

    if (topPreserve.length > 0) {
      console.log(chalk.green('\n✅ Top files to preserve:'));
      for (const file of topPreserve) {
        console.log(chalk.white(`  ${file.path} (score: ${file.qualityScore})`));
      }
    }

    // Show files to review
    const needReview = report.recommendations.review.slice(0, 3);
    if (needReview.length > 0) {
      console.log(chalk.yellow('\n⚠️  Files needing review:'));
      for (const file of needReview) {
        console.log(chalk.white(`  ${file.path} (score: ${file.qualityScore})`));
      }
    }

    // Show files to skip
    const toSkip = report.recommendations.skip
      .sort((a, b) => a.qualityScore - b.qualityScore)
      .slice(0, 3);

    if (toSkip.length > 0) {
      console.log(chalk.red('\n❌ Files safe to skip:'));
      for (const file of toSkip) {
        console.log(chalk.white(`  ${file.path} (score: ${file.qualityScore})`));
      }
    }
  }

  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

// Run CLI if this file is executed directly
if (require.main === module) {
  const cli = new FilePreservationCLI();
  cli.run().catch(error => {
    console.error(chalk.red('Fatal error:'), error.message);
    process.exit(1);
  });
}

module.exports = FilePreservationCLI;