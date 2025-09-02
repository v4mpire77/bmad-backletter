import { test, expect } from '@playwright/test';

// Verifies analyses fetched from the API appear on the list page.
test('lists analyses from API', async ({ page }) => {
  const analyses = [
    { id: '1', name: 'Contract A', status: 'complete' },
    { id: '2', name: 'Contract B', status: 'pending' },
  ];

  await page.route('**/api/analyses', route =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(analyses),
    })
  );

  await page.goto('/analyses');
  await expect(page.getByText('Contract A')).toBeVisible();
  await expect(page.getByText('Contract B')).toBeVisible();
});
