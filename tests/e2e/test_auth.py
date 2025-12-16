import pytest
from playwright.sync_api import Page

def test_register(page: Page, base_url):
    page.goto(f"{base_url}/register")
    page.fill("input[name='username']", "e2euser")
    page.fill("input[name='email']", "e2euser@example.com")
    page.fill("input[name='password']", "Password123!")
    page.click("text=Register")
    # Should redirect to login page
    assert page.url.endswith("/login")

def test_login(page: Page, base_url):
    page.goto(f"{base_url}/login")
    page.fill("input[name='username']", "e2euser")
    page.fill("input[name='password']", "Password123!")
    page.click("text=Login")
    # Should redirect to calculations page
    assert page.url.endswith("/calculations-page")
