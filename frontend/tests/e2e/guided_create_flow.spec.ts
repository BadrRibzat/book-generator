import { test, expect, Page, Locator } from '@playwright/test';

const TEST_USER = {
  username: 'testuser',
  password: 'test123',
};

async function signIn(page: Page) {
  await page.goto('/auth/signin');
  await page.waitForLoadState('domcontentloaded');
  await page.getByLabel(/username/i).fill(TEST_USER.username);
  await page.getByLabel(/^password$/i).fill(TEST_USER.password);
  await page.getByRole('button', { name: /sign in/i }).click();
  await expect(page.getByRole('link', { name: /profile/i })).toBeVisible({ timeout: 15000 });
}

async function navigateToMyBooks(page: Page) {
  await page.goto('/profile/books');
  await expect(page.getByRole('heading', { name: /my books/i })).toBeVisible({ timeout: 15000 });
}

async function selectRandomOptionLabel(options: Locator): Promise<{ text: string; value: string | null }> {
  const visibleIndexes: number[] = [];
  const total = await options.count();

  for (let index = 0; index < total; index += 1) {
    if (await options.nth(index).isVisible()) {
      visibleIndexes.push(index);
    }
  }

  if (visibleIndexes.length === 0) {
    throw new Error('No visible options available to select.');
  }

  const randomIndex = visibleIndexes[Math.floor(Math.random() * visibleIndexes.length)];
  const label = options.nth(randomIndex);

  const input = label.locator('input');
  await input.check({ force: true });

  const textContent = (await label.innerText()).replace(/\s+/g, ' ').trim();
  const value = (await input.getAttribute('value')) ?? null;

  return { text: textContent, value };
}

async function chooseRandomRadio(page: Page, heading: RegExp, inputName: string) {
  await page.getByRole('heading', { name: heading }).waitFor({ timeout: 15000 });

  const options = page.locator(`label:has(input[name="${inputName}"])`);
  await expect(options.first()).toBeVisible({ timeout: 15000 });

  const selection = await selectRandomOptionLabel(options);
  console.info(`[guided-flow] selected ${inputName}: ${selection.text} (${selection.value ?? 'n/a'})`);

  if (inputName === 'domain' && selection.value) {
    await page.waitForResponse((response) => {
      return response.url().includes(`/api/niches/?domain=${selection.value}`) && response.ok();
    });
  }
}

async function clickPrimary(page: Page) {
  await page.getByRole('button', { name: /(continue|generate my book)/i }).click();
}

test('guided create flow covers login, my books, and guided creation', async ({ page }) => {
  test.slow();

  await signIn(page);
  await navigateToMyBooks(page);

  await test.step('Start guided book creation', async () => {
    await page.getByRole('link', { name: /create new book/i }).click();
    await page.waitForURL('/profile/create');
    const domainResponse = page.waitForResponse((response) => response.url().includes('/api/domains') && response.ok());
    await page.waitForLoadState('domcontentloaded');
    await domainResponse;
  });

  await test.step('Select domain', async () => {
    await chooseRandomRadio(page, /choose your book domain/i, 'domain');
    await clickPrimary(page);
  });

  await test.step('Select niche', async () => {
    await chooseRandomRadio(page, /select your specific niche/i, 'niche');
    await clickPrimary(page);
  });

  await test.step('Select cover style', async () => {
    await chooseRandomRadio(page, /choose your cover style/i, 'cover_style');
    await clickPrimary(page);
  });

  await test.step('Select book length', async () => {
    await chooseRandomRadio(page, /choose your book length/i, 'book_length');
    await clickPrimary(page);
  });

  await test.step('Review configuration', async () => {
    await page.getByRole('heading', { name: /review your book configuration/i }).waitFor({ timeout: 15000 });
    await expect(page.locator('text=Structured Outline')).toBeVisible({ timeout: 15000 });
    await page.getByRole('button', { name: /generate my book/i }).click();
  });

  await test.step('Verify redirect to book details', async () => {
    await page.waitForURL(/\/profile\/books\/\d+$/, { timeout: 60000 });
    await expect(page.getByText(/generation progress/i)).toBeVisible({ timeout: 60000 });
  });
});
