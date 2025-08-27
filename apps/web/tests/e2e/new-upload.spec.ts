import { test } from '@playwright/test';

test.skip('mock upload stepper progresses and CTA routes', async ({ page }) => {
  await page.goto('/new');
});

