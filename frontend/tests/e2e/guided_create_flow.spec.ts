import { test, expect, Page } from '@playwright/test';

// Helper to sign in with default credentials
async function signIn(page: Page) {
  await page.goto('/auth/signin');
  await page.waitForLoadState('domcontentloaded');
  await page.getByLabel(/username/i).fill('testuser');
  await page.getByLabel(/^password$/i).fill('test123');
  await page.getByRole('button', { name: /sign in/i }).click();
  await expect(page.getByRole('link', { name: /profile/i })).toBeVisible({ timeout: 15000 });
}

// Select the first available tile option in the current step (label wrapping an input)
async function selectFirstTileUnder(page: Page, headingText: RegExp) {
  // Find the visible section that contains the step heading, then click its first tile
  const section = page.locator('div:has(> h2)').filter({ has: page.getByRole('heading', { name: headingText }) });
  await section.first().waitFor({ state: 'visible' });
  const option = section
    .locator('label')
    .filter({ has: page.locator('input[type="radio"], input[type="checkbox"]') })
    .filter({ hasText: /./ })
    .first();
  await option.waitFor({ state: 'visible' });
  await option.scrollIntoViewIfNeeded();
  await option.click();
}

// Select at least one topic checkbox
async function selectFirstTopic(page: Page) {
  const topic = page.locator('label:has(input[type="checkbox"])').first();
  await topic.click();
}

// Click the primary Continue/Generate button
async function clickPrimary(page: Page) {
  await page.getByRole('button', { name: /(continue|generate)/i }).click();
}

test('guided create flow redirects to book details', async ({ page }) => {
  test.slow(); // This flow loads several API lists and triggers book creation

  await signIn(page);
  await page.goto('/profile/create');
  await page.waitForLoadState('domcontentloaded');

  // Step 1: Domain
  await page.getByRole('heading', { name: /choose your book domain/i }).waitFor();
  await selectFirstTileUnder(page, /choose your book domain/i);
  await clickPrimary(page);

  // Step 2: Niche
  await page.getByRole('heading', { name: /select your specific niche/i }).waitFor();
  await selectFirstTileUnder(page, /select your specific niche/i);
  await clickPrimary(page);

  // Step 3: Book Style
  await page.getByRole('heading', { name: /choose your book style/i }).waitFor();
  await selectFirstTileUnder(page, /choose your book style/i);
  await clickPrimary(page);

  // Step 4: Cover Style
  await page.getByRole('heading', { name: /choose your cover style/i }).waitFor();
  await selectFirstTileUnder(page, /choose your cover style/i);
  await clickPrimary(page);

  // Step 5: Length
  await page.getByRole('heading', { name: /choose your book length/i }).waitFor();
  await selectFirstTileUnder(page, /choose your book length/i);
  await clickPrimary(page);

  // Step 6: Audience
  await page.getByRole('heading', { name: /define your target audience/i }).waitFor();
  await selectFirstTileUnder(page, /define your target audience/i);
  await clickPrimary(page);

  // Step 7: Key Topics
  await page.getByRole('heading', { name: /select key topics/i }).waitFor();
  await selectFirstTopic(page);
  await clickPrimary(page);

  // Step 8: Writing Preferences
  await page.getByRole('heading', { name: /writing style preferences/i }).waitFor();
  await selectFirstTileUnder(page, /writing style preferences/i);
  await clickPrimary(page);

  // Step 9: Confirm - Generate My Book
  await page.getByRole('heading', { name: /review your book configuration/i }).waitFor();
  await page.getByRole('button', { name: /generate my book/i }).click();

  // Expect to land on book details page
  await expect(page).toHaveURL(/\/profile\/books\/\d+/, { timeout: 60000 });
  // The details page usually shows status/progress; assert something generic is visible
  await expect(page.locator('body')).toContainText(/generat|processing|cover/i, { timeout: 60000 });
});
