const { test, expect } = require('@playwright/test');

test('api health reachable', async ({ page }) => {
  const api = process.env.NEXT_PUBLIC_API_URL || 'https://bmad-backletter.onrender.com';
  const res = await page.evaluate(async (apiUrl) => {
    const r = await fetch(`${apiUrl}/health`);
    return { ok: r.ok, text: await r.text() };
  }, api);
  expect(res.ok).toBeTruthy();
});
