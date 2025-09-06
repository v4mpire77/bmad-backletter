# Smart File Preservation System

An intelligent file management system for the BMAD Method that provides enhanced capabilities for preserving, analyzing, and migrating files based on quality assessment.

## 🎯 Problem Solved

The traditional approach to "saving good files" during migrations and cleanups often results in:
- Manual, time-consuming file selection
- Loss of valuable files due to poor naming or location
- Preservation of junk files that waste space
- No systematic approach to identify file quality
- Duplicate files consuming unnecessary storage

This system solves these problems with intelligent, automated file quality assessment and preservation strategies.

## 🚀 Features

### 1. File Quality Analysis
- **Comprehensive scoring system** (0-100) based on multiple factors:
  - File size and content analysis
  - Filename quality assessment
  - Content type and extension evaluation
  - Age and modification recency
  - Content patterns and structure analysis

### 2. Smart Preservation Modes
- **Intelligent Mode**: Balanced approach using multiple quality factors
- **Conservative Mode**: Only preserve high-quality, important files
- **Aggressive Mode**: Preserve most files except obvious junk

### 3. Intelligent Deduplication
- Hash-based duplicate detection
- Quality-based selection of best version
- Automatic removal of inferior duplicates

### 4. Backup Strategies
- Critical file identification
- Tiered backup planning (immediate/scheduled/versioned)
- Smart backup execution

### 5. Enhanced Integration
- Extends existing BMAD file manager
- Backward compatible with current tools
- CLI interface for standalone use

## 📁 File Structure

```
file-preservation/
├── file-quality-analyzer.js      # Core quality analysis engine
├── smart-preservation-manager.js # Main preservation orchestrator
├── enhanced-file-manager.js      # Enhanced BMAD file manager
├── file-preserve-cli.js          # Command-line interface
├── test-preservation.js          # Comprehensive test suite
└── README.md                     # This documentation
```

## 🛠️ Installation

The file preservation system is integrated into the BMAD Method tools. No separate installation required.

## 📖 Usage

### CLI Usage

```bash
# Analyze file quality in a directory
node file-preserve-cli.js analyze ./my-project --output analysis-report.json

# Smart file preservation
node file-preserve-cli.js preserve ./legacy-code --mode intelligent --dest ./preserved

# Find and clean duplicates
node file-preserve-cli.js clean-dupes ./documents --execute

# Create backup strategy
node file-preserve-cli.js backup ./critical-files --execute --dest ./backups

# View latest preservation report
node file-preserve-cli.js report --verbose
```

### Programmatic Usage

```javascript
const SmartFilePreservationManager = require('./smart-preservation-manager');
const FileQualityAnalyzer = require('./file-quality-analyzer');

// Analyze files
const analyzer = new FileQualityAnalyzer();
const analyses = await analyzer.analyzeDirectory('./source-path');
const report = analyzer.generateQualityReport(analyses);

// Preserve files
const manager = new SmartFilePreservationManager({
  preservationMode: 'intelligent',
  minQualityThreshold: 40
});

const result = await manager.preserveFiles('./source-path');
```

### Integration with BMAD File Manager

```javascript
const enhancedFileManager = require('./enhanced-file-manager');

// Enable smart preservation
enhancedFileManager.enableSmartPreservation({
  mode: 'intelligent',
  threshold: 40
});

// Copy directory with quality analysis
await enhancedFileManager.copyDirectoryWithSmartPreservation(
  './source', 
  './destination',
  { minQuality: 30, verbose: true }
);

// Create smart backup
await enhancedFileManager.createSmartBackup(
  './important-files',
  './backup',
  { includeStrategy: true }
);
```

## 🎯 Quality Scoring System

Files are scored from 0-100 based on weighted factors:

### Size Quality (20% weight)
- Empty files: 0 points
- Too small (<10 bytes): 20 points  
- Too large (>100MB): 30 points
- Good range (1KB-10MB): 80 points

### Name Quality (15% weight)
- Descriptive names: +10 points
- Version indicators: +15 points
- Junk patterns (temp, copy, untitled): -30 points
- Too short (<3 chars): -20 points

### Extension Quality (20% weight)
- High-value types (code, docs, config): +30 points
- Low-value extensions (.tmp, .bak): -40 points
- No extension: -10 points

### Content Quality (30% weight)
- Substantial content (>10 lines): +20 points
- Rich patterns (functions, classes): +25 points
- High duplication ratio: -30 points

### Age Quality (15% weight)
- Recently modified (<7 days): +20 points
- Recently active (<30 days): +10 points
- Stale (>365 days): -15 points

## 📊 Content Type Classification

Files are automatically classified into categories:
- **code**: .js, .ts, .py, .java, .cpp, etc.
- **documentation**: .md, .txt, .pdf, .docx
- **configuration**: .yaml, .yml, .json, .toml, .ini
- **image**: .jpg, .png, .gif, .svg
- **archive**: .zip, .tar, .gz
- **binary**: .exe, .dll, .so
- **other**: Everything else

## 🔄 Preservation Strategies

### Intelligent Mode (Default)
- Preserve files with quality score ≥ 40
- Special handling for important content types
- Consider valuable patterns even in lower-scored files

### Conservative Mode
- Only preserve high-quality files (≥ 80 score)
- Important file types with good quality (≥ 70)
- Minimal false positives

### Aggressive Mode  
- Preserve most files except obvious junk
- Include files with score ≥ 20
- Maximum preservation with some false positives

## 📈 Reports and Analysis

The system generates comprehensive reports including:
- Quality score distribution
- Content type breakdown
- Preservation recommendations
- Duplicate analysis
- Space savings calculations
- Action logs

Reports are saved in JSON format for further analysis or integration.

## 🧪 Testing

Run the comprehensive test suite:

```bash
node test-preservation.js
```

This creates test files with various quality characteristics and validates:
- Quality analysis accuracy
- Preservation strategy effectiveness
- Deduplication functionality
- Report generation
- File integrity

## 🔧 Configuration Options

### FileQualityAnalyzer Options
```javascript
{
  minFileSize: 1,              // Minimum file size in bytes
  maxFileSize: 100 * 1024 * 1024, // Maximum file size (100MB)
  textExtensions: ['.md', '.txt', '.js', ...],
  codeExtensions: ['.js', '.ts', '.py', ...],
  ignorePatterns: ['node_modules/**', '.git/**', ...]
}
```

### SmartFilePreservationManager Options
```javascript
{
  preservationMode: 'intelligent', // 'intelligent'|'conservative'|'aggressive'
  minQualityThreshold: 40,        // Minimum quality score to preserve
  deduplicate: true,              // Enable duplicate detection
  preservationRoot: './preserved', // Where to save preserved files
  analysisRoot: './analysis'      // Where to save analysis reports
}
```

## 🎯 Best Practices

1. **Start with Analysis**: Always run analysis first to understand your files
2. **Use Conservative Mode**: For critical migrations where precision matters
3. **Test First**: Use dry-run modes before executing destructive operations
4. **Review Reports**: Check preservation reports for unexpected results
5. **Backup Strategies**: Create backup strategies for critical files
6. **Quality Thresholds**: Adjust thresholds based on your specific needs

## 🔗 Integration Points

This system integrates with:
- BMAD Method file manager
- BMAD upgrader tools
- Project migration workflows
- Backup and archival processes
- CI/CD pipelines for file management

## 🚀 Future Enhancements

Planned improvements:
- Machine learning-based quality scoring
- Integration with version control systems
- Cloud storage optimization
- Performance optimizations for very large repositories
- Plugin system for custom quality factors
- Web-based dashboard for analysis visualization

## 📝 License

Part of the BMAD Method toolkit. See main project license.

## 🤝 Contributing

Contributions welcome! Please follow the BMAD Method contribution guidelines.

---

*This system represents a significant improvement over manual file selection and basic copying tools, providing intelligent, automated file preservation that saves time and ensures valuable files are never lost.*