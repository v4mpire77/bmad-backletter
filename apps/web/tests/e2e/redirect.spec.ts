import { test, expect } from '@playwright/test';

test('root redirects to /landing', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveURL(/\/landing$/);
});
