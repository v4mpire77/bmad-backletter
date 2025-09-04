# Coding Standards

## Type Sharing

All data models and types shared between the frontend and backend will reside in the packages/shared directory.

## API Calls

The frontend will use a dedicated service layer for all API interactions; no direct fetch calls in components.

## Environment Variables

Access environment variables only through dedicated configuration modules, never directly via process.env.

## Error Handling

All API routes must use a standardized error handling middleware to ensure consistent error responses.

## Database Access

The backend will use the Repository Pattern; no direct ORM calls from the router/controller layer.
