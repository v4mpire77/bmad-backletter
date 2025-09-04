# UX Specification

This document provides the current UX specification for Blackletter Systems.

## Wireframes

High-level wireframes covering the dashboard, contract upload, and findings views are maintained in [Figma](https://www.figma.com/file/blackletter/ux-spec). Exported images are available for offline review.

## User Flows

1. **Upload Contract**
   - User selects **Upload** from the dashboard.
   - System validates file type and size.
   - Job processing screen displays progress.
   - Findings page presents rule verdicts with evidence.
2. **Review Findings**
   - Filter by obligation or verdict.
   - Download the PDF report from the action menu.

## Accessibility Notes

- All interactive elements meet WCAG 2.1 AA color contrast requirements.
- Page content is fully navigable via keyboard with a logical focus order.
- Form inputs use associated labels and ARIA attributes.

See [`ux-mockups.md`](./ux-mockups.md) for high-fidelity mockups and visual references.
