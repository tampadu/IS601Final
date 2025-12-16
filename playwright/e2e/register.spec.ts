import { test, expect } from '@playwright/test';

test('register new user', async ({ page }) => {
  await page.goto('http://localhost:8000/register.html');
  await page.fill('input[name=email]', 'user1@test.com');
  await page.fill('input[name=password]', 'password123');
  await page.click('button[type=submit]');
  await expect(page.locator('#msg')).toHaveText('Registered!');
});
