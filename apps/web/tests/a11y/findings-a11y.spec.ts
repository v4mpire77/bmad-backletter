import { test } from '@playwright/test';

test.skip('findings table a11y basics', async ({ page }) => {
  await page.goto('/analyses/mock-1');
});

