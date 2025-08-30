import { defineConfig } from '@playwright/test';
import path from 'path';

const runDev = process.platform === 'win32' ? 'npm.cmd run dev' : 'npm run dev';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',
    headless: true,
  },
  webServer: [
    {
      command: runDev,
      cwd: path.join(process.cwd(), 'apps/web'),
      port: 3000,
      reuseExistingServer: !process.env.CI,
    },
  ],
});

