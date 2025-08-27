# Frontend Architecture Document

This document outlines the frontend architecture for the Blackletter project.

## 1. Template and Framework Selection

- **Framework:** Next.js 14
- **Language:** TypeScript
- **UI Library:** shadcn/ui + Radix + lucide-react
- **Styling:** Tailwind CSS
- **State Management:** React Query for server state
- **Testing:** Playwright for E2E tests and Vitest for UI tests

## 2. Frontend Tech Stack

| Category | Technology | Version | Purpose | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| Framework | Next.js | 14.2.x | The core framework for the frontend application. | Enables server components, simple routing, and a modern React development experience. |
| UI Library | shadcn/ui | latest | A collection of reusable UI components. | Provides a solid foundation of accessible and customizable components built on Radix UI. |
| State Management | React Query | 5.x | For managing server state, caching, and data fetching. | Simplifies data fetching, caching, and synchronization with the backend. |
| Routing | Next.js App Router | 14.2.x | Handles all client-side and server-side routing. | Integrated into Next.js, providing a simple and powerful routing solution. |
| Build Tool | Next.js | 14.2.x | The build tool for the Next.js application. | Integrated into Next.js, providing an optimized build process out of the box. |
| Styling | Tailwind CSS | 3.4.x | A utility-first CSS framework for styling the application. | Enables rapid UI development with a consistent and maintainable styling system. |
| Testing | Playwright, Vitest | latest | For end-to-end and unit/UI testing. | Provides a comprehensive testing strategy covering the entire application. |
| Component Library | shadcn/ui | latest | The primary component library for the application. | A set of high-quality, accessible, and customizable components. |
| Form Handling | react-hook-form | latest | For building and managing forms. | A performant and easy-to-use library for form handling in React. |
| Animation | | | | |
| Dev Tools | ESLint, Prettier | latest | For code linting and formatting. | Enforces a consistent code style and helps to prevent common errors. |

## 3. Project Structure

```
apps/web/
  app/
    layout.tsx
    page.tsx                   # landing/login (or upload)
    dashboard/
      page.tsx
      loading.tsx
      error.tsx
    analyses/
      [id]/
        page.tsx                 # findings table + evidence drawer
        loading.tsx
        error.tsx
    settings/
      page.tsx
  src/
    components/
      ui/                        # shadcn components (generated)
      charts/
      layout/
      feedback/                  # toasts, banners, dialogs
    features/
      upload/
        UploadDropzone.tsx
        useUpload.ts
      findings/
        FindingsTable.tsx
        EvidenceDrawer.tsx
        VerdictChip.tsx
      reports/
        ExportDialog.tsx
      metrics/
        MetricsTiles.tsx
    lib/
      api/
        client.ts                # typed client (OpenAPI or fetch wrapper)
        queries.ts               # React Query hooks
        types.ts                 # shared DTOs if needed
      utils.ts
      env.ts                     # zod‑validated env
    styles/
      globals.css
      tailwind.css
    hooks/
      useDisclosure.ts           # simple local state helper
    providers/
      QueryProvider.tsx
      ThemeProvider.tsx
  public/
  tests/
    e2e/                         # Playwright
    ui/                          # Vitest + RTL
  package.json
  tsconfig.json
```

## 4. Component Standards

### Component Template

```typescript
// Location: src/components/MyComponent.tsx

import type { PropsWithChildren } from 'react';

interface MyComponentProps {
  /** A brief description of the prop. */
  exampleProp: string;
}

/**
 * @description A brief, one-sentence description of what MyComponent does.
 * @param {MyComponentProps} props - The props for the component.
 */
export const MyComponent = ({ exampleProp }: MyComponentProps) => {
  return (
    <div>
      {/* Component JSX */}
      <p>{exampleProp}</p>
    </div>
  );
};

// --- Optional: For components that explicitly need to accept children ---

// Use TypeScript's utility type `PropsWithChildren` to add the children prop.
type ComponentWithChildrenProps = PropsWithChildren<MyComponentProps>;

export const ComponentWithChildren = ({ exampleProp, children }: ComponentWithChildrenProps) => {
  return (
    <div>
      <p>{exampleProp}</p>
      {children}
    </div>
  );
};
```

### Naming Conventions

- **Components:** `PascalCase.tsx`
- **Files:** `PascalCase.tsx` for components, `kebab-case.ts` for all other files.
- **Services:** `.service.ts` suffix (e.g., `auth.service.ts`).
- **State Management:** `.store.ts` suffix (e.g., `upload.store.ts`).
- **Hooks:** `useCamelCase.ts` (e.g., `useDisclosure.ts`).
- **Types and Interfaces:** `PascalCase` for both.

## 5. State Management

### Store Structure

```
src/
  features/
    [feature-name]/
      state.ts       # Zustand store for this feature (if needed)
```

### State Management Template

```typescript
// Location: src/features/[feature-name]/state.ts
import { create } from 'zustand';

// 1. Define the interface for both STATE and ACTIONS
interface FeatureState {
  // --- STATE ---
  /** Brief description of the property. */
  exampleProperty: string;

  // --- ACTIONS ---
  /** Brief description of the action. */
  setExampleProperty: (value: string) => void;
  /** Resets the state to its initial values. */
  reset: () => void;
}

// 2. Define the initial state object
// Use `Pick` for type safety, ensuring we only define state properties.
const initialState: Pick<FeatureState, 'exampleProperty'> = {
  exampleProperty: 'initial value',
};

// 3. Create and export the store's hook in one step
export const useFeatureState = create<FeatureState>((set) => ({
  ...initialState,

  // --- ACTION IMPLEMENTATIONS ---
  setExampleProperty: (value) => set({ exampleProperty: value }),
  reset: () => set(initialState),
}));
```

## 6. API Integration

### Service Template

```typescript
// Location: src/lib/api/services/uploads.service.ts

import { apiClient, isApiError } from '../client'; // Assuming client exports an error type guard
import type { paths } from '../types'; // Assuming types are generated from OpenAPI

// Extracting the specific type for the successful response
type UploadSuccessResponse = paths['/contracts']['post']['responses']['201']['content']['application/json'];

export const uploadsService = {
  /**
   * Uploads a contract file to the backend.
   * @param file The contract file to upload.
   * @returns The response data on successful upload.
   * @throws A normalized Error if the API call fails.
   */
  uploadContract: async (file: File): Promise<UploadSuccessResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await apiClient.post('/contracts', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      // Log the raw error for debugging purposes
      console.error('API Error in uploadContract:', error);

      // Use a type guard to check if it's a structured API error from our client
      if (isApiError(error)) {
        // Re-throw a more user-friendly or normalized error message
        const message = error.response?.data?.message || 'Server error during file upload.';
        throw new Error(message);
      }

      // Throw a generic error for all other cases (e.g., network failure)
      throw new Error('An unexpected error occurred. Please check your connection.');
    }
  },
};
```

### API Client Configuration

```typescript
// Location: src/lib/api/client.ts

import axios, { AxiosError } from 'axios';
import { env } from '@/lib/env'; // <-- Import the validated env object

// 1. Define a standard shape for our API errors
export interface ApiErrorData {
  code: string;
  message: string;
  hint?: string;
}

// 2. Create a type guard to check for our specific API error shape
export const isApiError = (error: unknown): error is AxiosError<ApiErrorData> => {
  return axios.isAxiosError(error) && error.response?.data?.code !== undefined;
};

// 3. Create and configure the Axios instance
export const apiClient = axios.create({
  baseURL: env.NEXT_PUBLIC_API_BASE_URL, // <-- Use the type-safe, validated URL
  withCredentials: true, // Important for session cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// 4. Optional: Add interceptors for auth or global error logging if needed
// (For MVP, we can keep this minimal and add interceptors later)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // We could add global logging here if desired, but for now,
    // we will let the individual service methods handle their own errors.
    return Promise.reject(error);
  }
);
```

### React Query Hooks

```typescript
// Location: src/lib/api/hooks/[resource].hooks.ts

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { uploadsService } from '../services/uploads.service';
import { queryKeys } from '../keys'; // <-- Import the factory

// --- Query Hook using the factory ---
export const useAnalysisQuery = (analysisId: string) => {
  return useQuery({
    queryKey: queryKeys.analyses.detail(analysisId), // <-- Use the factory
    queryFn: () => uploadsService.getAnalysis(analysisId),
    enabled: !!analysisId,
  });
};

// --- Mutation Hook using the factory for invalidation ---
export const useUploadContractMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (file: File) => uploadsService.uploadContract(file),
    onSuccess: () => {
      // <-- Invalidate with the factory for type-safe consistency
      queryClient.invalidateQueries({ queryKey: queryKeys.analyses.lists() });
    },
    onError: (error: Error) => {
      console.error('Upload failed:', error.message);
      // Show toast notification, etc.
    },
  });
};
```

## 7. Routing

### Route Configuration

```typescript
// Location: middleware.ts (in the root of the project)

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// 1. Define which routes are public and which are protected
const protectedRoutes = ['/dashboard', '/analyses', '/settings'];
const publicRoutes = ['/login', '/signup'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const sessionToken = request.cookies.get('session_token')?.value;

  // 2. Redirect to login if trying to access a protected route without a session
  if (protectedRoutes.some((path) => pathname.startsWith(path)) && !sessionToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 3. Redirect to dashboard if trying to access a public route with a session
  if (publicRoutes.some((path) => pathname.startsWith(path)) && sessionToken) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    // Match all routes except for static assets and internal Next.js routes
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

## 8. Styling Guidelines

### Styling Approach

The project will use **Tailwind CSS** as its primary styling solution. This utility-first CSS framework will be used for all component and layout styling.

### Global Theme Variables

```css
/* Location: src/styles/globals.css */

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;

    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;

    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;

    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;

    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;

    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;

    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;

    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;

    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;

    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;

    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;

    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;

    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;

    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;

    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 210 40% 98%;
  }
}
```

## 9. Testing Requirements

### Component Test Template

```typescript
// Location: tests/ui/components/[component-name].test.tsx

import { render, screen } from './test-utils'; // <-- Import our custom render
import userEvent from '@testing-library/user-event';
import { MyComponent } from '@/components/MyComponent';
import { describe, it, expect, vi } from 'vitest';

// --- 1. Mocking Dependencies ---
// Example: If MyComponent calls an external service, we mock it here.
const mockSomeService = {
  performAction: vi.fn().mockResolvedValue({ success: true }),
};

// Use vi.mock to replace the actual service with our mock implementation
vi.mock('@/lib/services/some.service', () => ({
  someService: mockSomeService,
}));


describe('MyComponent', () => {
  // --- 2. Test the Initial Render ---
  it('should render correctly with initial props', () => {
    render(<MyComponent exampleProp="test value" />);
    
    // Assert that the initial state is correct
    expect(screen.getByText('test value')).toBeInTheDocument();
  });

  // --- 3. Test User Interactions ---
  it('should call the service action when the button is clicked', async () => {
    // Best practice: set up userEvent for realistic interactions
    const user = userEvent.setup();
    render(<MyComponent exampleProp="test value" />);

    // Find the element by its accessible role, which is more robust than by text
    const actionButton = screen.getByRole('button', { name: /perform action/i });
    
    // Simulate a user clicking the button
    await user.click(actionButton);

    // Assert that our mock function was called as expected
    expect(mockSomeService.performAction).toHaveBeenCalledOnce();
  });
  
  // Add more tests for different states (loading, error) and interactions...
});
```

### Testing Best Practices

1.  **Unit Tests**: Test individual components in isolation.
2.  **Integration Tests**: Test component interactions.
3.  **E2E Tests**: Test critical user flows (using Playwright).
4.  **Coverage Goals**: Aim for 80% code coverage.
5.  **Test Structure**: Arrange-Act-Assert pattern.
6.  **Mock External Dependencies**: API calls, routing, state management.

## 10. Environment Configuration

```
# .env.local (for local development - DO NOT COMMIT)

# Next.js
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api

# Backend (for reference, not used by the frontend)
# DATABASE_URL="file:./dev.db"
# SECRET_KEY="your-secret-key"
```

## 11. Frontend Developer Standards

### Critical Coding Rules

1.  **State Management:**
    *   Use React Query for all server state. Do not use `useEffect` to fetch data.
    *   For client-side state, use local component state (`useState`, `useReducer`) first. Only introduce a Zustand store when state needs to be shared between multiple, non-parent/child components.
2.  **Styling:**
    *   Always use utility classes from Tailwind CSS for styling.
    *   Do not use inline styles or create separate CSS files for components.
    *   For reusable style compositions, use the `@apply` directive in `src/styles/globals.css` as previously discussed.
3.  **API Integration:**
    *   All API calls must go through the defined service layer (`src/lib/api/services`).
    *   Do not use `fetch` or `axios` directly in components.
    *   Always use the React Query hooks (`src/lib/api/hooks`) to interact with the API from components.
4.  **Environment Variables:**
    *   Always import environment variables from the validated `src/lib/env.ts` module.
    *   Do not access `process.env` directly in the application code.
5.  **Dependencies:**
    *   Do not install new dependencies without approval.
    *   All new dependencies must be added to the `package.json` file.

### Quick Reference

*   **Common Commands:**
    *   `npm run dev`: Start the development server.
    *   `npm run build`: Build the application for production.
    *   `npm run start`: Start the production server.
    *   `npm run test`: Run the test suite.
    *   `npm run lint`: Run the linter.
    *   `npm run format`: Format the code with Prettier.
*   **Key Import Patterns:**
    *   `import { MyComponent } from '@/components/MyComponent';`
    *   `import { useMyHook } from '@/hooks/useMyHook';`
    *   `import { myService } from '@/lib/api/services/my.service';`
    *   `import { useMyQuery } from '@/lib/api/hooks/my.hooks';`
*   **File Naming Conventions:**
    *   Components: `PascalCase.tsx`
    *   Hooks: `useCamelCase.ts`
    *   Services: `kebab-case.service.ts`
    *   Stores: `kebab-case.store.ts`
    *   Other files: `kebab-case.ts`
*   **Project-Specific Patterns:**
    *   **State Management:** Use local state first. If global state is needed, create a Zustand store in the relevant `src/features` directory.
    *   **API Calls:** Use the React Query hooks in `src/lib/api/hooks`.
    *   **Styling:** Use Tailwind CSS utility classes.
