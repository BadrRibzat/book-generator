import { test, expect } from '@playwright/test';

// Sanity: Sign In page renders and form fields are accessible

test('sign in form renders and validates', async ({ page }) => {
  await page.goto('/auth/signin');
  // Avoid flakiness from background requests; wait for DOM to be ready and key heading to appear
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('heading', { name: /welcome back/i })).toBeVisible();

  await expect(page.getByLabel(/username/i)).toBeVisible();
  await expect(page.getByLabel(/^password$/i)).toBeVisible();
  await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible();
});
