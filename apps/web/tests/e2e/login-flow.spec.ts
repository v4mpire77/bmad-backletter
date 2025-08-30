import { test, expect } from '@playwright/test';

test('user logs in and is redirected to dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="username"]', 'user@example.com');
  await page.fill('input[name="password"]', 'strongPassword');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');
  const token = await page.evaluate(() => localStorage.getItem('access_token'));
  expect(token).toBeTruthy();
});
