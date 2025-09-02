import { test, expect } from '@playwright/test';

test('home page and nav to upload works', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveURL('/');
  await page.getByRole('link', { name: 'Upload' }).click();
  await expect(page).toHaveURL(/\/upload$/);
});
