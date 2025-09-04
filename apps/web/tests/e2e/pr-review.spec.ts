import { test, expect } from '@playwright/test';

const repoSlug = process.env.TEST_REPO_SLUG;

test.describe('PR review flow', () => {
  test.skip(!repoSlug, 'Requires TEST_REPO_SLUG env var with seeded test repository');

  test.beforeEach(async ({ page }) => {
    await page.goto(`/repos/${repoSlug}/pull/1/files`);
  });

  test('add and resolve comment in file diff', async ({ page }) => {
    await page.getByRole('link', { name: /README.md/i }).click();
    await page.getByRole('button', { name: /add comment/i }).click();
    await page.getByPlaceholder('Leave a comment').fill('Looks good');
    await page.getByRole('button', { name: /^comment$/i }).click();
    await page.getByRole('button', { name: /resolve conversation/i }).click();
  });

  test('switch between files using keyboard shortcuts', async ({ page }) => {
    await page.keyboard.press('j');
    await expect(page).toHaveURL(/file=2/);
    await page.keyboard.press('k');
    await expect(page).toHaveURL(/file=1/);
  });

  test('warn on unsaved comment when navigating', async ({ page }) => {
    await page.getByRole('link', { name: /README.md/i }).click();
    await page.getByPlaceholder('Leave a comment').fill('Unsaved comment');
    await page.getByRole('link', { name: /package.json/i }).click();
    await expect(page.getByText('You have unsaved comments')).toBeVisible();
  });
});
