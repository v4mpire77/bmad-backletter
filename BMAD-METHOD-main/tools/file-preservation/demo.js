#!/usr/bin/env node

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
  dim: (text) => `\x1b[2m${text}\x1b[0m`,
  bold: (text) => `\x1b[1m${text}\x1b[0m`,
  orange: (text) => `\x1b[38;5;208m${text}\x1b[0m`
};

const FileQualityAnalyzer = require('./file-quality-analyzer');

/**
 * Practical demonstration of the file preservation system
 * Analyzes real repository files and shows preservation recommendations
 */
async function demonstrateFilePreservation() {
  console.log(chalk.bold(chalk.blue('\n🚀 Smart File Preservation System Demo')));
  console.log(chalk.blue('='.repeat(60)));
  console.log(chalk.white('This demo analyzes files in the current repository to show'));
  console.log(chalk.white('how the smart preservation system identifies good files to save.\n'));

  const repoRoot = path.resolve(__dirname, '../../..');
  
  try {
    // Create analyzer with repository-appropriate settings
    const analyzer = new FileQualityAnalyzer({
      ignorePatterns: [
        'node_modules/**',
        '.git/**',
        '**/*.log',
        '**/test-files/**',
        '**/node_modules/**',
        '**/.venv/**',
        '**/pnpm-lock.yaml',
        '**/package-lock.json'
      ]
    });

    console.log(chalk.yellow('🔍 Analyzing repository files...'));
    console.log(chalk.dim(`Repository root: ${repoRoot}`));

    // Analyze a subset of directories to avoid overwhelming output
    const dirs = ['docs', 'apps', 'BMAD-METHOD-main/tools', 'scripts'];
    let allAnalyses = [];

    for (const dir of dirs) {
      const dirPath = path.join(repoRoot, dir);
      try {
        await fsPromises.access(dirPath);
        console.log(chalk.dim(`  Analyzing ${dir}/...`));
        const analyses = await analyzer.analyzeDirectory(dirPath, { 
          recursive: true, 
          includeHidden: false 
        });
        allAnalyses = allAnalyses.concat(analyses);
      } catch (error) {
        console.log(chalk.dim(`  Skipping ${dir}/ (not found)`));
      }
    }

    // If main directories aren't found, analyze specific files in root
    if (allAnalyses.length === 0) {
      console.log(chalk.yellow('  Analyzing repository root files...'));
      console.log(chalk.dim(`  Looking in: ${repoRoot}`));
      
      // Analyze some common file types in the root
      const rootFiles = await fsPromises.readdir(repoRoot);
      console.log(chalk.dim(`  Found ${rootFiles.length} files in root`));
      
      const interestingFiles = rootFiles.filter(file => 
        file.endsWith('.md') || 
        file.endsWith('.js') || 
        file.endsWith('.json') ||
        file.endsWith('.yml') ||
        file.endsWith('.yaml') ||
        file.endsWith('.py')
      );

      console.log(chalk.dim(`  Filtering to ${interestingFiles.length} interesting files`));

      for (const file of interestingFiles) {
        const filePath = path.join(repoRoot, file);
        try {
          const analysis = await analyzer.analyzeFile(filePath);
          allAnalyses.push(analysis);
          console.log(chalk.dim(`    ✅ Analyzed: ${file}`));
        } catch (error) {
          console.log(chalk.dim(`    ❌ Error analyzing ${file}: ${error.message}`));
        }
      }

      // Also analyze our new preservation tools as examples
      const preservationDir = path.join(repoRoot, 'BMAD-METHOD-main/tools/file-preservation');
      try {
        await fsPromises.access(preservationDir);
        console.log(chalk.dim('  Analyzing file-preservation tools...'));
        const analyses = await analyzer.analyzeDirectory(preservationDir, { 
          recursive: false, 
          includeHidden: false 
        });
        allAnalyses = allAnalyses.concat(analyses.filter(a => !a.path.includes('test-files')));
      } catch (error) {
        // Ignore if not found
      }
    }

    if (allAnalyses.length === 0) {
      console.log(chalk.yellow('⚠️  No files found to analyze'));
      return;
    }

    console.log(chalk.green(`✅ Analyzed ${allAnalyses.length} files`));

    // Generate comprehensive report
    const report = analyzer.generateQualityReport(allAnalyses);

    // Display executive summary
    console.log(chalk.blue('\n📊 EXECUTIVE SUMMARY'));
    console.log(chalk.blue('-'.repeat(40)));
    console.log(chalk.white(`📁 Total files analyzed: ${report.totalFiles}`));
    console.log(chalk.white(`📈 Average quality score: ${report.averageScore}/100`));
    console.log(chalk.white(`💾 Total size: ${formatBytes(report.summary.totalSize)}`));

    // Quality distribution
    console.log(chalk.blue('\n📈 Quality Distribution:'));
    console.log(chalk.green(`  🔥 High (80-100): ${report.scoreDistribution.high} files`));
    console.log(chalk.yellow(`  👍 Medium (60-79): ${report.scoreDistribution.medium} files`));
    console.log(chalk.orange(`  👎 Low (40-59): ${report.scoreDistribution.low} files`));
    console.log(chalk.red(`  💀 Poor (0-39): ${report.scoreDistribution.poor} files`));

    // Content type analysis
    console.log(chalk.blue('\n📂 Content Type Distribution:'));
    const sortedTypes = Object.entries(report.contentTypes)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 8);
    
    for (const [type, count] of sortedTypes) {
      const icon = getContentTypeIcon(type);
      console.log(chalk.white(`  ${icon} ${type}: ${count} files`));
    }

    // Top preservation candidates
    if (report.recommendations.preserve.length > 0) {
      console.log(chalk.blue('\n🏆 TOP PRESERVATION CANDIDATES'));
      console.log(chalk.blue('-'.repeat(40)));
      const topFiles = report.recommendations.preserve
        .sort((a, b) => b.qualityScore - a.qualityScore)
        .slice(0, 10);

      for (const file of topFiles) {
        const icon = getContentTypeIcon(file.contentType);
        const score = file.qualityScore;
        const scoreColor = score >= 80 ? chalk.green : score >= 60 ? chalk.yellow : chalk.orange;
        console.log(`  ${icon} ${scoreColor(score.toString().padStart(2, ' '))}/100 ${chalk.white(file.path)}`);
      }
    }

    // Files needing review
    if (report.recommendations.review.length > 0) {
      console.log(chalk.blue('\n⚠️  FILES NEEDING REVIEW'));
      console.log(chalk.blue('-'.repeat(40)));
      const reviewFiles = report.recommendations.review
        .sort((a, b) => b.qualityScore - a.qualityScore)
        .slice(0, 5);

      for (const file of reviewFiles) {
        const icon = getContentTypeIcon(file.contentType);
        console.log(`  ${icon} ${chalk.yellow(file.qualityScore.toString().padStart(2, ' '))}/100 ${chalk.white(file.path)}`);
      }
    }

    // Files safe to skip
    if (report.recommendations.skip.length > 0) {
      console.log(chalk.blue('\n🗑️  FILES SAFE TO SKIP'));
      console.log(chalk.blue('-'.repeat(40)));
      const skipFiles = report.recommendations.skip
        .sort((a, b) => a.qualityScore - b.qualityScore)
        .slice(0, 5);

      for (const file of skipFiles) {
        const icon = getContentTypeIcon(file.contentType);
        console.log(`  ${icon} ${chalk.red(file.qualityScore.toString().padStart(2, ' '))}/100 ${chalk.dim(file.path)}`);
      }
    }

    // Duplicate analysis
    if (report.duplicates.length > 0) {
      console.log(chalk.blue('\n🔄 DUPLICATE ANALYSIS'));
      console.log(chalk.blue('-'.repeat(40)));
      console.log(chalk.cyan(`Found ${report.duplicates.length} groups of duplicate files`));
      
      const totalDuplicateSize = report.duplicates.reduce((sum, d) => 
        sum + (d.duplicateCount * d.files[0].size), 0
      );
      console.log(chalk.cyan(`Potential space savings: ${formatBytes(totalDuplicateSize)}`));

      // Show a few examples
      const exampleDuplicates = report.duplicates.slice(0, 3);
      for (const group of exampleDuplicates) {
        console.log(chalk.white(`\n  📂 Duplicate group (${group.files.length} files):`));
        console.log(chalk.green(`    ✅ Best: ${group.bestFile.path} (score: ${group.bestFile.qualityScore})`));
        for (const dup of group.files.slice(1)) {
          console.log(chalk.red(`    ❌ Remove: ${dup.path} (score: ${dup.qualityScore})`));
        }
      }
    }

    // Preservation strategy recommendations
    console.log(chalk.blue('\n💡 PRESERVATION STRATEGY RECOMMENDATIONS'));
    console.log(chalk.blue('-'.repeat(50)));
    
    const preserveCount = report.recommendations.preserve.length;
    const reviewCount = report.recommendations.review.length;
    const skipCount = report.recommendations.skip.length;
    const totalFiles = preserveCount + reviewCount + skipCount;

    if (totalFiles > 0) {
      const preservePercent = Math.round((preserveCount / totalFiles) * 100);
      const reviewPercent = Math.round((reviewCount / totalFiles) * 100);
      const skipPercent = Math.round((skipCount / totalFiles) * 100);

      console.log(chalk.green(`🎯 Preserve immediately: ${preserveCount} files (${preservePercent}%)`));
      console.log(chalk.yellow(`🔍 Review manually: ${reviewCount} files (${reviewPercent}%)`));
      console.log(chalk.red(`⏭️  Safe to skip: ${skipCount} files (${skipPercent}%)`));

      // Storage optimization
      const preserveSize = report.recommendations.preserve.reduce((sum, f) => sum + (f.size || 0), 0);
      const skipSize = report.recommendations.skip.reduce((sum, f) => sum + (f.size || 0), 0);
      
      console.log(chalk.blue('\n💾 Storage Impact:'));
      console.log(chalk.white(`  Preserve: ${formatBytes(preserveSize)}`));
      console.log(chalk.white(`  Can skip: ${formatBytes(skipSize)}`));
      if (skipSize > 0) {
        const savingsPercent = Math.round((skipSize / (preserveSize + skipSize)) * 100);
        console.log(chalk.cyan(`  Space savings: ${savingsPercent}%`));
      }
    }

    // Usage recommendations
    console.log(chalk.blue('\n🛠️  USAGE RECOMMENDATIONS'));
    console.log(chalk.blue('-'.repeat(40)));
    console.log(chalk.white('Based on this analysis, here are the recommended next steps:'));
    console.log('');
    
    if (report.scoreDistribution.high > 0) {
      console.log(chalk.green('✅ High-quality files detected - definitely preserve these'));
    }
    
    if (report.duplicates.length > 0) {
      console.log(chalk.cyan('🔄 Run deduplication to save space and reduce clutter'));
    }
    
    if (report.recommendations.skip.length > 10) {
      console.log(chalk.yellow('🧹 Consider cleaning up low-quality files to reduce repository size'));
    }
    
    if (report.scoreDistribution.poor > report.totalFiles * 0.2) {
      console.log(chalk.orange('⚠️  High percentage of poor-quality files - review cleanup strategy'));
    }

    console.log('');
    console.log(chalk.dim('💡 Use the CLI tools to execute preservation strategies:'));
    console.log(chalk.dim('   node file-preserve-cli.js preserve ./path --mode intelligent'));
    console.log(chalk.dim('   node file-preserve-cli.js clean-dupes ./path --execute'));

    console.log(chalk.blue('\n' + '='.repeat(60)));
    console.log(chalk.green('🎉 Analysis complete! Use the insights above to improve file management.'));

  } catch (error) {
    console.error(chalk.red('❌ Demo failed:'), error.message);
    if (error.stack) {
      console.error(chalk.dim(error.stack));
    }
  }
}

function getContentTypeIcon(type) {
  const icons = {
    code: '⚡',
    documentation: '📚',
    configuration: '⚙️',
    image: '🖼️',
    video: '🎬',
    audio: '🎵',
    archive: '📦',
    binary: '🔧',
    other: '📄'
  };
  return icons[type] || '📄';
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// Run demo if this file is executed directly
if (require.main === module) {
  demonstrateFilePreservation().catch(error => {
    console.error(chalk.red('Demo execution failed:'), error.message);
    process.exit(1);
  });
}

module.exports = { demonstrateFilePreservation };