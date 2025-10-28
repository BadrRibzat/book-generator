import { test, expect } from '@playwright/test';

// Basic smoke test: app boots, header nav is present, and we can navigate to Sign In

test('home page renders with accessible navigation', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const nav = page.locator('nav');
  await expect(nav).toBeVisible();

  // On desktop the Sign In link is visible; if not, open mobile menu and retry
  const signInLink = page.getByRole('link', { name: /sign in/i });
  if (!(await signInLink.isVisible())) {
    const menuBtn = page.getByRole('button').filter({ hasText: /☰|bars/i });
    if (await menuBtn.count()) {
      await menuBtn.first().click();
    } else {
      // fallback: click the only visible button in header (mobile menu)
      await page.locator('header button').first().click({ trial: true }).catch(() => {});
      await page.locator('header button').first().click().catch(() => {});
    }
  }

  // Now either Sign In or Profile should be present
  const profileLink = page.getByRole('link', { name: /profile/i });
  await expect(signInLink.or(profileLink)).toBeVisible();
});
