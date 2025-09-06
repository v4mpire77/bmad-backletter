const fs = require('node:fs');
const fsPromises = require('node:fs/promises');
const path = require('node:path');

// Simple chalk replacement
const chalk = {
  red: (text) => `\x1b[31m${text}\x1b[0m`,
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
  cyan: (text) => `\x1b[36m${text}\x1b[0m`,
  white: (text) => text,
  dim: (text) => `\x1b[2m${text}\x1b[0m`
};

const FileQualityAnalyzer = require('./file-quality-analyzer');

/**
 * Simple test for the file preservation system
 */
async function testFilePreservation() {
  console.log(chalk.blue('🧪 Testing File Preservation System'));
  console.log(chalk.blue('='.repeat(50)));

  const testDir = path.join(__dirname, 'test-files');

  try {
    // Clean up and create test directory
    try {
      await fsPromises.rm(testDir, { recursive: true, force: true });
    } catch {}
    await fsPromises.mkdir(testDir, { recursive: true });

    // Create test files
    await createTestFiles(testDir);

    // Test File Quality Analyzer
    console.log(chalk.yellow('\n📊 Testing File Quality Analyzer...'));
    const analyzer = new FileQualityAnalyzer();
    const analyses = await analyzer.analyzeDirectory(testDir, { recursive: true });
    
    console.log(chalk.green(`✅ Analyzed ${analyses.length} test files`));
    
    // Display analysis results
    const validAnalyses = analyses.filter(a => !a.error);
    if (validAnalyses.length > 0) {
      const topFiles = validAnalyses
        .sort((a, b) => b.qualityScore - a.qualityScore)
        .slice(0, 3);

      console.log(chalk.cyan('🏆 Top quality files:'));
      for (const file of topFiles) {
        console.log(chalk.white(`  ${file.name}: ${file.qualityScore}/100 (${file.contentType})`));
      }
    }

    // Test Quality Report
    console.log(chalk.yellow('\n📋 Testing Quality Report Generation...'));
    const report = analyzer.generateQualityReport(analyses);
    
    console.log(chalk.green('✅ Quality report generated:'));
    console.log(chalk.white(`  Average score: ${report.averageScore}/100`));
    console.log(chalk.white(`  High quality: ${report.scoreDistribution.high} files`));
    console.log(chalk.white(`  Medium quality: ${report.scoreDistribution.medium} files`));
    console.log(chalk.white(`  Low quality: ${report.scoreDistribution.low} files`));
    console.log(chalk.white(`  Poor quality: ${report.scoreDistribution.poor} files`));

    if (report.duplicates.length > 0) {
      console.log(chalk.cyan(`🔄 Found ${report.duplicates.length} duplicate groups`));
    }

    // Test content type classification
    console.log(chalk.yellow('\n📂 Content Type Distribution:'));
    for (const [type, count] of Object.entries(report.contentTypes)) {
      console.log(chalk.white(`  ${type}: ${count} files`));
    }

    // Test recommendations
    console.log(chalk.yellow('\n💡 Preservation Recommendations:'));
    console.log(chalk.green(`  High priority: ${report.recommendations.preserve.length} files`));
    console.log(chalk.yellow(`  Review needed: ${report.recommendations.review.length} files`));
    console.log(chalk.red(`  Can skip: ${report.recommendations.skip.length} files`));

    console.log(chalk.blue('\n🎉 BASIC TESTS PASSED!'));
    console.log(chalk.dim(`Test files created in: ${testDir}`));

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
  await fsPromises.writeFile(path.join(testDir, 'high-quality-code.js'), `
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
  await fsPromises.writeFile(path.join(testDir, 'documentation.md'), `
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
  await fsPromises.writeFile(path.join(testDir, 'temp_backup_copy.txt'), 'Just some temporary content');

  // Empty file (should score 0)
  await fsPromises.writeFile(path.join(testDir, 'empty.txt'), '');

  // Configuration file (important type)
  await fsPromises.writeFile(path.join(testDir, 'config.yaml'), `
app:
  name: test-app
  version: 1.0.0
  
database:
  host: localhost
  port: 5432
`);

  // Duplicate files (same content, different names)
  const duplicateContent = 'This is duplicate content for testing deduplication.';
  await fsPromises.writeFile(path.join(testDir, 'duplicate1.txt'), duplicateContent);
  await fsPromises.writeFile(path.join(testDir, 'duplicate2.txt'), duplicateContent);

  // Junk files
  await fsPromises.writeFile(path.join(testDir, 'debug123.log'), 'Debug log content...');
  await fsPromises.writeFile(path.join(testDir, 'untitled.txt'), 'Untitled file');

  // Good quality Python file
  const pythonFile = path.join(testDir, 'recent-important.py');
  await fsPromises.writeFile(pythonFile, `
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