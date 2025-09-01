<<<<<<< HEAD
# Blackletter GDPR Processor - Frontend Dockerfile
# Context Engineering Framework v2.0.0 Compliant
# Multi-stage build for optimized production deployment

# ---- Dependencies Stage ----
FROM node:20-alpine AS deps
=======
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

<<<<<<< HEAD
# Install dependencies with cache optimization
RUN npm ci --only=production --frozen-lockfile

# ---- Builder Stage ----
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files and dependencies
COPY package.json package-lock.json* ./
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production
=======
# Install dependencies
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set environment variables
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a

# Build the application
RUN npm run build

<<<<<<< HEAD
# ---- Runtime Stage ----
FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Set environment variables
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "server.js"]
=======
# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
