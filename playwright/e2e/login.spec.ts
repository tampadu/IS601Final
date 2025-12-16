import { test, expect } from '@playwright/test';

test('login with correct credentials', async ({ page }) => {
  await page.goto('http://localhost:8000/login.html');
  await page.fill('input[name=email]', 'user1@test.com');
  await page.fill('input[name=password]', 'password123');
  await page.click('button[type=submit]');
  await expect(page.locator('#msg')).toHaveText('Logged in!');
});
