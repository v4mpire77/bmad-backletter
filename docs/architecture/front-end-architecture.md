# Blackletter Frontend Architecture Document

This document outlines the architectural strategy and technical implementation details for the Blackletter frontend application, a core part of the larger full-stack system. It is designed to be a single source of truth for UI development, ensuring consistency, performance, and accessibility.

## 1. Template and Framework Selection

The frontend for this project will be a Single-Page Application (SPA) built on **Next.js 14** using the **App Router**. It will be developed in **TypeScript**. The project will leverage a monorepo structure with the frontend code housed in the `apps/web/` directory.

## 2. Frontend Tech Stack

The following technologies and tools have been selected to build the frontend application:
| Category | Technology | Version | Purpose |
|---|---|---|---|
| Framework | Next.js | 14.x | Frontend application with server-side rendering and routing. |
| UI Component Library | shadcn/ui | latest | Accessible, customizable components that provide a design system foundation. |
| Styling | Tailwind CSS | latest | Utility-first CSS framework for rapid and consistent styling. |
| State Management | React Query | latest | Manages server-side state, data fetching, and caching, for the API. |
| Testing | Playwright, Vitest | latest | Comprehensive testing coverage. |

## 3. Project Structure

The file layout for the frontend application will follow a feature-based organization within the `apps/web/src` directory:

```
apps/web/src/
├── app/                  # Next.js App Router pages (e.g., /dashboard)
├── features/             # Feature-specific components (e.g., /dashboard)
├── components/           # Reusable, non-feature components (e.g., MockModeBanner.tsx)
├── lib/                  # Hooks, API clients, utilities, and types
├── public/               # Static assets (images, fonts)
└── styles/               # Global CSS and tokens
```

## 4. Component Standards

All components will be built with React and TypeScript, using shadcn/ui and Tailwind for styling. A feature-based component organization will be used to promote reusability and maintainability.

## 5. State Management

  - **Server State**: All data fetching from the API will be managed by **React Query**. This includes caching and synchronizing data for the dashboard's KPIs and recent analyses lists.
  - **Client State**: Local UI state will be managed using standard React Hooks (`useState`, `useReducer`), as appropriate.

## 6. API Integration

API integration will be handled using a custom client wrapper around React Query. This service layer will manage all API calls, including authentication and error handling, ensuring that components don't have direct knowledge of the API endpoints.

## 7. Routing

Routing is handled by the **Next.js App Router**. Key routes include:

  - `/dashboard`: The main home page, listing KPIs and recent analyses.
  - `/new` or `/upload`: The document upload flow.
  - `/analyses/[id]`: A dynamic route for a full details view of an analysis.

## 8. Styling Guidelines

The styling approach will be based on **Tailwind CSS**, a utility-first CSS framework. A global CSS file will be used for foundational styles and fonts. Components from **shadcn/ui** will provide the base for a consistent and accessible design system.

## 9. Testing Requirements

  - **Unit Tests**: Vitest will be used for isolated component tests.
  - **E2E Tests**: **Playwright** will be used for end-to-end testing of critical user flows, including dashboard rendering, navigation, and mobile responsiveness.
  - **Accessibility Testing**: We will aim for a Lighthouse **Accessibility ≥ 90** score and ensure **WCAG AA contrast** and semantic headings are in place.

## 10. Performance Budgets

The following performance budgets are defined to ensure a fast and responsive user experience:

  - **LCP (Largest Contentful Paint)**: ≤ 2.5s on the `/dashboard` route.
  - **p95 Interaction Latency**: ≤ 150ms for client-side interactions like filtering and sorting.
  - **p95 List Fetch**: ≤ 600ms for fetching the list of recent analyses.
