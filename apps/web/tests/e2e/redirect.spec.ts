import { test, expect } from '@playwright/test';

test('root redirects to /upload and nav works', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveURL(/\/upload$/);
  await page.getByRole('link', { name: 'Analyses' }).click();
  await expect(page).toHaveURL(/\/analyses$/);
});
