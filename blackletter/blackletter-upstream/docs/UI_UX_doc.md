# UI/UX Design Documentation

## Design System Specifications

### Brand Identity
- **Primary Color:** Deep Blue (#1E3A8A) - Represents trust, professionalism, and legal expertise
- **Secondary Color:** Gold (#F59E0B) - Represents quality, precision, and value
- **Accent Color:** Emerald Green (#059669) - Represents compliance, safety, and success
- **Neutral Colors:** 
  - Light Gray (#F9FAFB) - Background
  - Medium Gray (#6B7280) - Text secondary
  - Dark Gray (#111827) - Text primary

### Typography
- **Primary Font:** Inter - Modern, readable, professional
- **Secondary Font:** JetBrains Mono - For code and technical content
- **Font Weights:** 400 (Regular), 500 (Medium), 600 (Semi-bold), 700 (Bold)
- **Font Sizes:**
  - H1: 2.25rem (36px)
  - H2: 1.875rem (30px)
  - H3: 1.5rem (24px)
  - H4: 1.25rem (20px)
  - Body: 1rem (16px)
  - Small: 0.875rem (14px)
  - Caption: 0.75rem (12px)

### Spacing System
- **Base Unit:** 4px
- **Spacing Scale:** 4px, 8px, 12px, 16px, 20px, 24px, 32px, 40px, 48px, 64px, 80px, 96px
- **Container Padding:** 24px (desktop), 16px (tablet), 12px (mobile)
- **Component Spacing:** 16px between related elements, 24px between sections

## UI Component Guidelines

### Button Components
```typescript
// Primary Button
<Button variant="default" size="default">
  Analyze Document
</Button>

// Secondary Button
<Button variant="secondary" size="default">
  Upload File
</Button>

// Destructive Button
<Button variant="destructive" size="default">
  Delete Analysis
</Button>

// Ghost Button
<Button variant="ghost" size="default">
  Cancel
</Button>
```

### Card Components
```typescript
// Analysis Result Card
<Card className="p-6">
  <CardHeader>
    <CardTitle>Contract Analysis Results</CardTitle>
    <CardDescription>GDPR Compliance Check</CardDescription>
  </CardHeader>
  <CardContent>
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span>Compliance Score</span>
        <Badge variant="success">85%</Badge>
      </div>
    </div>
  </CardContent>
</Card>
```

### Form Components
```typescript
// File Upload
<div className="space-y-4">
  <Label htmlFor="document">Upload Document</Label>
  <Input
    id="document"
    type="file"
    accept=".pdf,.doc,.docx,.txt"
    className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
  />
  <p className="text-sm text-gray-500">
    Supported formats: PDF, DOC, DOCX, TXT (Max 10MB)
  </p>
</div>
```

### Table Components
```typescript
// Analysis Results Table
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Issue Type</TableHead>
      <TableHead>Severity</TableHead>
      <TableHead>Location</TableHead>
      <TableHead>Recommendation</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {findings.map((finding) => (
      <TableRow key={finding.id}>
        <TableCell>{finding.type}</TableCell>
        <TableCell>
          <Badge variant={finding.severity === 'high' ? 'destructive' : 'warning'}>
            {finding.severity}
          </Badge>
        </TableCell>
        <TableCell>Page {finding.page}</TableCell>
        <TableCell>{finding.recommendation}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

## User Experience Flow Diagrams

### Document Analysis Flow
```
1. User lands on dashboard
   ↓
2. Clicks "Upload Document" or drags file
   ↓
3. File validation and processing
   ↓
4. Analysis progress indicator
   ↓
5. Results display with:
   - Compliance score
   - Issues found
   - Recommendations
   - Download report option
   ↓
6. User can:
   - Download detailed report
   - Share results
   - Start new analysis
```

### RAG System Flow
```
1. User navigates to RAG interface
   ↓
2. Uploads or selects documents for knowledge base
   ↓
3. System processes and indexes documents
   ↓
4. User asks questions or queries
   ↓
5. System retrieves relevant context
   ↓
6. Displays answer with source references
   ↓
7. User can:
   - Ask follow-up questions
   - View source documents
   - Export conversation
```

### Vague Terms Detection Flow
```
1. User uploads contract document
   ↓
2. System scans for vague terms
   ↓
3. Highlights problematic phrases
   ↓
4. Provides explanations and risks
   ↓
5. Suggests alternative language
   ↓
6. User can:
   - Accept suggestions
   - Modify manually
   - Ignore warnings
   ↓
7. Generate revised document
```

## Responsive Design Requirements

### Breakpoints
- **Mobile:** 320px - 768px
- **Tablet:** 768px - 1024px
- **Desktop:** 1024px - 1440px
- **Large Desktop:** 1440px+

### Mobile-First Approach
```css
/* Base styles (mobile) */
.container {
  padding: 12px;
  max-width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 16px;
    max-width: 768px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 24px;
    max-width: 1024px;
  }
}
```

### Responsive Components
- **Navigation:** Collapsible hamburger menu on mobile
- **Tables:** Horizontal scroll or card layout on mobile
- **Forms:** Stacked layout on mobile, side-by-side on desktop
- **Charts:** Simplified versions on mobile with full detail on desktop

## Accessibility Standards

### WCAG 2.1 AA Compliance
- **Color Contrast:** Minimum 4.5:1 ratio for normal text
- **Keyboard Navigation:** All interactive elements accessible via keyboard
- **Screen Reader Support:** Proper ARIA labels and semantic HTML
- **Focus Indicators:** Visible focus states for all interactive elements

### Accessibility Features
```typescript
// Proper labeling
<Button aria-label="Upload document for analysis">
  <UploadIcon />
  Upload
</Button>

// Screen reader announcements
<div role="status" aria-live="polite">
  Analysis complete. Found 3 compliance issues.
</div>

// Keyboard navigation
<div tabIndex={0} onKeyDown={handleKeyDown}>
  Interactive content
</div>
```

## Style Guide and Branding

### Logo Usage
- **Primary Logo:** Full color on light backgrounds
- **Secondary Logo:** Monochrome for dark backgrounds
- **Minimum Size:** 120px width for digital use
- **Clear Space:** Equal to the height of the "B" in Blackletter

### Icon System
- **Style:** Outlined icons with 2px stroke
- **Size:** 16px, 20px, 24px, 32px
- **Color:** Inherit from parent text color
- **Library:** Lucide React icons

### Visual Hierarchy
1. **Primary Actions:** Blue buttons with white text
2. **Secondary Actions:** Gray buttons with dark text
3. **Destructive Actions:** Red buttons with white text
4. **Information:** Blue badges and alerts
5. **Warnings:** Yellow/orange badges and alerts
6. **Success:** Green badges and alerts

## Component Library Organization

### Core Components
```
components/ui/
├── button.tsx
├── card.tsx
├── dialog.tsx
├── input.tsx
├── label.tsx
├── select.tsx
├── table.tsx
├── tabs.tsx
├── textarea.tsx
└── badge.tsx
```

### Business Components
```
components/
├── blackletter-app.tsx      # Main application wrapper
├── navigation.tsx           # Navigation component
├── document-upload.tsx      # File upload interface
├── analysis-results.tsx     # Results display
├── compliance-checker.tsx   # Compliance analysis
├── rag-interface.tsx        # RAG system interface
├── vague-terms-finder.tsx   # Vague terms detection
├── dashboard.tsx            # Main dashboard
└── charts/
    ├── compliance-chart.tsx
    ├── issues-chart.tsx
    └── progress-chart.tsx
```

## User Journey Maps

### New User Journey
1. **Landing Page:** Clear value proposition and features
2. **Sign Up:** Simple registration process
3. **Onboarding:** Guided tour of key features
4. **First Analysis:** Upload document with clear instructions
5. **Results:** Comprehensive analysis with explanations
6. **Next Steps:** Clear call-to-action for continued use

### Power User Journey
1. **Dashboard:** Quick access to recent analyses and tools
2. **Bulk Upload:** Multiple document processing
3. **Advanced Analysis:** Custom rules and configurations
4. **Team Collaboration:** Share results and collaborate
5. **API Integration:** Connect with existing workflows
6. **Reporting:** Generate comprehensive reports

## Wireframe References

### Dashboard Layout
```
┌─────────────────────────────────────────────────────────┐
│ Navigation Bar                                          │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│ │ Upload      │ │ Recent      │ │ Quick       │        │
│ │ Document    │ │ Analyses    │ │ Stats       │        │
│ └─────────────┘ └─────────────┘ └─────────────┘        │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Analysis Results Table                              │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Analysis Results Page
```
┌─────────────────────────────────────────────────────────┐
│ Navigation Bar                                          │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────────────────────────────┐ │
│ │ Document    │ │ Compliance Score: 85%               │ │
│ │ Info        │ │                                     │ │
│ │             │ │ Issues Found: 3                     │ │
│ │             │ │                                     │ │
│ └─────────────┘ └─────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Issues List                                          │ │
│ │ • GDPR Issue 1                                       │ │
│ │ • Vague Terms Issue 2                                │ │
│ │ • Compliance Issue 3                                 │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Design Tool Integration

### Figma Integration
- **Design System:** Centralized component library
- **Prototyping:** Interactive prototypes for user testing
- **Developer Handoff:** Automatic code generation
- **Version Control:** Design version history

### Design Tokens
```json
{
  "colors": {
    "primary": "#1E3A8A",
    "secondary": "#F59E0B",
    "accent": "#059669",
    "background": "#F9FAFB",
    "text": "#111827"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  },
  "typography": {
    "fontFamily": "Inter",
    "fontSizes": {
      "h1": "2.25rem",
      "h2": "1.875rem",
      "body": "1rem"
    }
  }
}
```

This UI/UX documentation provides a comprehensive guide for maintaining design consistency and creating a professional, accessible, and user-friendly interface for the Blackletter Systems application.
