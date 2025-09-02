# Authentication

This document outlines how Blackletter authenticates API requests and manages access across organizations.

## JWT Tokens

- The API uses JSON Web Tokens (JWT) for stateless authentication.
- Tokens are signed with the `HS256` algorithm using the `JWT_SECRET` environment variable.
- Standard claims include:
  - `sub`: user identifier.
  - `role`: user's role within the current organization.
  - `org_id`: organization the token is scoped to.
  - `exp`: expiration timestamp; tokens are short‑lived.
- Clients send the token in the `Authorization: Bearer <token>` header.

## Roles

Blackletter defines three roles:

| Role   | Capabilities                          |
|--------|---------------------------------------|
| admin  | manage users, organizations, and data |
| member | run analyses and view reports         |
| viewer | read‑only access to assigned reports  |

Role claims are embedded in each JWT. The API enforces permissions based on these roles.

## Organization Switching

Users belong to one or more organizations. A JWT is scoped to a single organization via the `org_id` claim.

To switch organizations:

1. Request a new token for the target organization (e.g., `POST /auth/switch-org`).
2. The server issues a JWT with the updated `org_id` claim.
3. Clients use the new token in subsequent requests.

This approach keeps authorization simple while enabling multi‑tenant access control.

