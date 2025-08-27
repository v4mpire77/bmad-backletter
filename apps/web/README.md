**Overview**

- Developer Guide (always-on): `docs/dev/always-on-dev-guide.md` — quick commands, agent flows, spec map

This is the web frontend for Blackletter, built with Next.js (App Router). In this monorepo, the web app lives under `apps/web` and the API (FastAPI) under `apps/api`.

**Local Development**

- Install deps: `npm install`
- Run dev: `npm run dev`
- Open: `http://localhost:3000`
- Default route: `/` redirects to `/dashboard` (see `src/app/page.tsx`).

**Project Structure (selected)**

- `src/app/page.tsx`: Root redirect to `/dashboard`.
- `src/app/dashboard/page.tsx`: Demo Dashboard (mock-enabled).
- `src/app/analyses/[id]/page.tsx`: Findings view with table, drawer, export dialog.
- `src/app/reports/page.tsx`: Reports (mock stub list).
- `src/components/*`: FindingsTable, EvidenceDrawer, VerdictChips, ExportDialog.
- `src/lib/mocks.ts`: Seeded UI mocks (enable via env).
- `src/lib/anchors.ts`: Detector → anchor terms for highlighting.

**Demo Mode (frontend-only)**

- Set `NEXT_PUBLIC_USE_MOCKS=1` (see `.env.example`).
- Visit `/dashboard` → open ACME_DPA_MOCK.pdf → navigate to `/analyses/mock-1`.
- Use Export in the Findings header to push a mock record and navigate to `/reports`.
- Unset `NEXT_PUBLIC_USE_MOCKS` to fall back to API stubs. Optionally set `NEXT_PUBLIC_API_BASE=http://localhost:8000`.

**Deployment: Vercel (Monorepo)**

1. **Create project:** In Vercel, click “New Project” and import your Git repository.
2. **Root directory:** Set the project’s Root Directory to `apps/web` (monorepo setting).
3. **Framework preset:** Vercel should auto-detect Next.js.
4. **Build settings:**
   - Install Command: `npm install`
   - Build Command: `next build` (default)
   - Output: `Next.js` (automatic)
5. **Env vars (optional):** Add `NEXT_PUBLIC_API_BASE_URL` when your API is deployed.
6. **Node version:** Use Node 18+ (Vercel default is fine for Next 15).
7. **Deploy:** Trigger the first deployment. Production URL will be provided by Vercel.

**Custom Domain**

- Add your domain in Vercel → Project → Settings → Domains. Point DNS as instructed by Vercel. `/` will render the landing page via redirect to `/landing`.

**API Deployment (FastAPI)**

- The API at `apps/api` is not deployed on Vercel. Recommended options: Fly.io, Railway, Render, or Azure Web Apps.
- After deploying the API, set `NEXT_PUBLIC_API_BASE_URL` in Vercel and update the web app to use it for HTTP calls.

**Troubleshooting**

- Demo not showing data: ensure `NEXT_PUBLIC_USE_MOCKS=1` and reload.
- API fallback failing: start API with `uvicorn blackletter_api.main:app --reload --app-dir ../api` and set `NEXT_PUBLIC_API_BASE`.

## Docker + Render (All-in-One)

- Local Docker: see `docs/deployment/docker-local.md`.
- Render deployment: see `render.yaml` and `docs/deployment/render.md` for one-click blueprint or dashboard setup.
- Runtime: Nginx proxies `/api/*` to FastAPI and other routes to Next.js SSR.
