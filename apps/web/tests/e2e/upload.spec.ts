import { test, expect } from '@playwright/test';

// Ensures a file upload transitions through to a success state
// without hitting live APIs.
test('upload completes successfully', async ({ page }) => {
  await page.route('**/api/intake', route =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ analysis_id: 'test-analysis' }),
    })
  );

  await page.route('**/api/analyses/test-analysis/file', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: '{}' })
  );

  await page.addInitScript(() => {
    class MockWebSocket {
      onmessage: ((ev: { data: string }) => void) | null = null;
      close() {}
      constructor() {
        const steps = [
          { step: 'extracting', progress: 25 },
          { step: 'detecting', progress: 50 },
          { step: 'reporting', progress: 75 },
          { step: 'done', progress: 100 },
        ];
        steps.forEach((msg, idx) => {
          setTimeout(() => this.onmessage?.({ data: JSON.stringify(msg) }), idx * 10);
        });
      }
    }
    // @ts-ignore
    window.WebSocket = MockWebSocket;
  });

  await page.goto('/new');
  await page.setInputFiles('input[type="file"]', {
    name: 'contract.txt',
    mimeType: 'text/plain',
    buffer: Buffer.from('hello world'),
  });

  await expect(page.getByRole('button', { name: 'View Findings' })).toBeVisible();
});
