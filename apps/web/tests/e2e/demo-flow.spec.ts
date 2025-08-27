import { test, expect } from '@playwright/test';

test.skip('demo flow: dashboard -> findings -> export -> reports', async ({ page }) => {
  // Placeholder skeleton; enable after wiring local server & data
  await page.goto('/dashboard');
  await expect(page).toHaveTitle(/Blackletter|Dashboard/i);
});

