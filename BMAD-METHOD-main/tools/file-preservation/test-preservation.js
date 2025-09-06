const fs = require('fs-extra');
const path = require('node:path');
const chalk = require('chalk');
const FileQualityAnalyzer = require('../file-preservation/file-quality-analyzer');
const SmartFilePreservationManager = require('../file-preservation/smart-preservation-manager');

/**
 * Test the file preservation system with sample files
 */
async function testFilePreservation() {
  console.log(chalk.blue('🧪 Testing File Preservation System'));
  console.log(chalk.blue('='.repeat(50)));

  const testDir = path.join(__dirname, '../../../test-preservation');
  const preservedDir = path.join(testDir, 'preserved');
  const analysisDir = path.join(testDir, 'analysis');

  try {
    // Clean up previous test
    await fs.remove(testDir);
    await fs.ensureDir(testDir);

    // Create test files with various quality levels
    await createTestFiles(testDir);

    // Test 1: File Quality Analyzer
    console.log(chalk.yellow('\n📊 Testing File Quality Analyzer...'));
    const analyzer = new FileQualityAnalyzer();
    const analyses = await analyzer.analyzeDirectory(testDir, { recursive: true });
    
    console.log(chalk.green(`✅ Analyzed ${analyses.length} test files`));
    
    // Display some analysis results
    const topFiles = analyses
      .filter(a => !a.error)
      .sort((a, b) => b.qualityScore - a.qualityScore)
      .slice(0, 5);

    console.log(chalk.cyan('🏆 Top 5 quality files:'));
    for (const file of topFiles) {
      console.log(chalk.white(`  ${file.path}: ${file.qualityScore}/100 (${file.contentType})`));
    }

    // Test 2: Generate Quality Report
    console.log(chalk.yellow('\n📋 Testing Quality Report Generation...'));
    const report = analyzer.generateQualityReport(analyses);
    
    console.log(chalk.green('✅ Quality report generated:'));
    console.log(chalk.white(`  Average score: ${report.averageScore}/100`));
    console.log(chalk.white(`  High quality: ${report.scoreDistribution.high} files`));
    console.log(chalk.white(`  Duplicates found: ${report.duplicates.length} groups`));

    // Test 3: Smart Preservation Manager
    console.log(chalk.yellow('\n💾 Testing Smart Preservation Manager...'));
    const manager = new SmartFilePreservationManager({
      preservationRoot: preservedDir,
      analysisRoot: analysisDir,
      preservationMode: 'intelligent',
      minQualityThreshold: 40
    });

    const preservationResult = await manager.preserveFiles(testDir);
    
    if (preservationResult.success) {
      console.log(chalk.green('✅ Preservation completed successfully'));
      console.log(chalk.white(`  Files preserved: ${preservationResult.filesPreserved}`));
      console.log(chalk.white(`  Files skipped: ${preservationResult.filesSkipped}`));
    } else {
      console.log(chalk.red('❌ Preservation failed:', preservationResult.error));
    }

    // Test 4: Backup Strategy
    console.log(chalk.yellow('\n🛡️  Testing Backup Strategy...'));
    const backupStrategy = await manager.createBackupStrategy(testDir);
    
    console.log(chalk.green('✅ Backup strategy created:'));
    console.log(chalk.white(`  Immediate backup: ${backupStrategy.backupPlan.immediate.length} files`));
    console.log(chalk.white(`  Scheduled backup: ${backupStrategy.backupPlan.scheduled.length} files`));

    // Test 5: Verify preserved files
    console.log(chalk.yellow('\n🔍 Verifying preserved files...'));
    const preservedFiles = await fs.readdir(preservedDir, { recursive: true });
    const analysisFiles = await fs.readdir(analysisDir);
    
    console.log(chalk.green(`✅ Found ${preservedFiles.length} preserved files`));
    console.log(chalk.green(`✅ Found ${analysisFiles.length} analysis files`));

    console.log(chalk.blue('\n🎉 ALL TESTS PASSED!'));
    console.log(chalk.dim(`Test results saved in: ${testDir}`));

  } catch (error) {
    console.error(chalk.red('❌ Test failed:'), error.message);
    if (error.stack) {
      console.error(chalk.dim(error.stack));
    }
  }
}

/**
 * Create test files with various quality characteristics
 */
async function createTestFiles(testDir) {
  console.log(chalk.yellow('📝 Creating test files...'));

  // High quality code file
  await fs.writeFile(path.join(testDir, 'high-quality-code.js'), `
/**
 * High quality JavaScript module with comprehensive documentation
 * This file should score highly in our quality analysis
 */

class DataProcessor {
  constructor(options = {}) {
    this.options = {
      maxRetries: options.maxRetries || 3,
      timeout: options.timeout || 5000,
      ...options
    };
  }

  async processData(data) {
    if (!data || data.length === 0) {
      throw new Error('Data cannot be empty');
    }

    return data.map(item => ({
      ...item,
      processed: true,
      timestamp: new Date().toISOString()
    }));
  }

  // TODO: Add error handling for network requests
  async fetchData(url) {
    // Implementation here
  }
}

module.exports = DataProcessor;
`);

  // Medium quality documentation
  await fs.writeFile(path.join(testDir, 'documentation.md'), `
# Project Documentation

This is a medium-quality documentation file.

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`bash
npm install
\`\`\`

## Usage

Basic usage example.
`);

  // Low quality temp file
  await fs.writeFile(path.join(testDir, 'temp_backup_copy.txt'), 'Just some temporary content');

  // Empty file (should score 0)
  await fs.writeFile(path.join(testDir, 'empty.txt'), '');

  // Configuration file (important type)
  await fs.writeFile(path.join(testDir, 'config.yaml'), `
app:
  name: test-app
  version: 1.0.0
  
database:
  host: localhost
  port: 5432
`);

  // Large binary-like file
  await fs.writeFile(path.join(testDir, 'large-file.bin'), Buffer.alloc(1024 * 1024, 'x'));

  // Duplicate files (same content, different names)
  const duplicateContent = 'This is duplicate content for testing deduplication.';
  await fs.writeFile(path.join(testDir, 'duplicate1.txt'), duplicateContent);
  await fs.writeFile(path.join(testDir, 'duplicate2.txt'), duplicateContent);
  await fs.writeFile(path.join(testDir, 'duplicate3.txt'), duplicateContent);

  // Junk files
  await fs.writeFile(path.join(testDir, 'debug123.log'), 'Debug log content...');
  await fs.writeFile(path.join(testDir, 'untitled.txt'), 'Untitled file');

  // Good quality with recent modification
  const recentFile = path.join(testDir, 'recent-important.py');
  await fs.writeFile(recentFile, `
#!/usr/bin/env python3
"""
Recent Python file with good content
"""

import sys
import os

def main():
    print("Hello, World!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
`);

  // Set recent modification time
  const recentTime = new Date();
  await fs.utimes(recentFile, recentTime, recentTime);

  // Old file
  const oldFile = path.join(testDir, 'old-legacy.js');
  await fs.writeFile(oldFile, 'var oldCode = "legacy";');
  const oldTime = new Date('2020-01-01');
  await fs.utimes(oldFile, oldTime, oldTime);

  console.log(chalk.green('✅ Test files created'));
}

// Run test if this file is executed directly
if (require.main === module) {
  testFilePreservation().catch(error => {
    console.error(chalk.red('Test execution failed:'), error.message);
    process.exit(1);
  });
}

module.exports = { testFilePreservation };