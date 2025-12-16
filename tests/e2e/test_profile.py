import pytest
from playwright.sync_api import Page

def test_profile_update(page: Page, base_url):
    page.goto(f"{base_url}/login")
    page.fill("input[name='username']", "e2euser")
    page.fill("input[name='password']", "Password123!")
    page.click("text=Login")

    page.goto(f"{base_url}/profile")
    page.fill("input[name='username']", "e2euser2")
    page.fill("input[name='email']", "e2euser2@example.com")
    page.click("text=Update Profile")

    # Should redirect back to profile page
    assert page.url.endswith("/profile")

def test_password_change(page: Page, base_url):
    page.goto(f"{base_url}/login")
    page.fill("input[name='username']", "e2euser2")
    page.fill("input[name='password']", "Password123!")
    page.click("text=Login")

    page.goto(f"{base_url}/profile/password")
    page.fill("input[name='current_password']", "Password123!")
    page.fill("input[name='new_password']", "NewPass123!")
    page.fill("input[name='confirm_new_password']", "NewPass123!")
    page.click("text=Change Password")

    assert page.url.endswith("/profile")
