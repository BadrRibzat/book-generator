import { test, expect, Page } from '@playwright/test';

// End-to-end: sign in with known credentials and land on Profile
// Credentials provided by repo setup docs
const USERNAME = 'testuser';
const PASSWORD = 'test123';

// Helper to sign in
async function signIn(page: Page) {
  await page.goto('/auth/signin');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('heading', { name: /welcome back/i })).toBeVisible();

  await page.getByLabel(/username/i).fill(USERNAME);
  await page.getByLabel(/^password$/i).fill(PASSWORD);
  await page.getByRole('button', { name: /sign in/i }).click();
}

test('user can sign in and see profile links', async ({ page }) => {
  await signIn(page);

  // After sign-in, we may stay on the same route; wait for the header to update
  const profileLink = page.getByRole('link', { name: /profile/i });
  await expect(profileLink).toBeVisible({ timeout: 15000 });

  // Navigate to Profile to confirm access and auth guard passes
  await Promise.all([
    page.waitForURL(/\/profile(\/?|$)/, { timeout: 15000 }).catch(() => {}),
    profileLink.click(),
  ]);
  // Final assertion: we are on /profile
  await expect(page).toHaveURL(/\/profile(\/?|$)/);
});
