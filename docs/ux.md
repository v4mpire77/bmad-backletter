# UX Summary

## Principles
- Evidence-first, deterministic wording
- Windows-friendly, low-cognition layouts
- WCAG AA accessible with keyboard navigation and screen reader labels

## Primary Flows
1. **Upload → Findings → Export**
   - User uploads PDF/DOCX via dropzone
   - Progress bar tracks extraction and detection
   - Findings table shows verdicts (green/amber/red/gray)
   - Evidence drawer reveals context spans and anchors
   - Export modal offers PDF/CSV/JSON
2. **History Recall**
   - List past analyses with search and filter
   - Open any analysis to view findings again
3. **Settings Toggle**
   - Manage rulepacks, retention, and accessibility preferences

## Components
- UploadDropzone
- ProgressBar
- FindingCard & FindingsTable
- EvidenceDrawer
- HistoryTable
- SettingsToggles
- Toast notifications

## Visual Tokens
- Font: Inter
- Colors: Slate/white surfaces, verdict colors {#16a34a, #f59e0b, #dc2626, #6b7280}
- Icons: Lucide

## States
- Loading, empty, success, error states for each component
