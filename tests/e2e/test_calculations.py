import pytest
from playwright.sync_api import Page

def test_add_calculation(page: Page, base_url):
    page.goto(f"{base_url}/login")
    page.fill("input[name='username']", "e2euser")
    page.fill("input[name='password']", "Password123!")
    page.click("text=Login")
    
    page.goto(f"{base_url}/calculations-page")
    # Example form inputs; adjust selectors if using HTML inputs
    page.fill("input[name='a']", "10")
    page.fill("input[name='b']", "5")
    page.select_option("select[name='type']", "Add")
    page.click("text=Calculate")

    # Validate result is displayed
    result_text = page.text_content("#result")
    assert "15" in result_text
