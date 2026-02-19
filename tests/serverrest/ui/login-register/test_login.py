import pytest
from tests.serverrest.config import ServerRestConfig 
from playwright.sync_api import Page, expect
from faker import Faker

from tests.serverrest.support.api_tasks import delete_user_by_email, create_user
from tests.serverrest.support.ui_tasks import login, register

faker = Faker()

@pytest.mark.ui
def test_login_page_loads(page: Page, serverrest_config: ServerRestConfig) -> None:
    """Go to login page and verify if the elements are visible."""
    page.goto(f"{serverrest_config.UI_BASE_URL}/login")
    expect(page.locator('input[data-testid="email"]')).to_be_visible()
    expect(page.locator('input[data-testid="senha"]')).to_be_visible()
    expect(page.locator('button[data-testid="entrar"]')).to_be_visible()

@pytest.mark.ui 
def test_login_with_unregistered_user(page: Page, serverrest_config: ServerRestConfig) -> None:
    """Try to login with an unregistered user and verify if the error message is visible."""
    page.goto(f"{serverrest_config.UI_BASE_URL}/login")
    login(page, "unregistered@example.com", "teste123")
    expect(page.locator('div.alert.alert-secondary')).to_be_visible(timeout=5000)

@pytest.mark.ui
def test_navigate_and_register(page: Page, serverrest_config: ServerRestConfig) -> None:
    """Go to register page and register a new user."""
    page.goto(f"{serverrest_config.UI_BASE_URL}/login")
    page.locator('a[data-testid="cadastrar"]').click()
    register(page, "John Doe", faker.email(), "password123")
    expect(page.locator('div.alert.alert-primary')).to_be_visible()

@pytest.mark.ui
def test_login_with_registered_user(page: Page, serverrest_config: ServerRestConfig, registered_user) -> None:
    """Create user via API, then login in UI."""
    page.goto(f"{serverrest_config.UI_BASE_URL}/login")
    login(page, registered_user["email"], registered_user["password"])
    expect(page.locator(f'.jumbotron h1:has-text("{registered_user["nome"]}")')).to_be_visible()
