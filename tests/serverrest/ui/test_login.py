import pytest
from playwright.sync_api import Page

from tests.serverrest.config import ServerRestConfig
from tests.serverrest.api.helpers.api_helpers import delete_user_by_email
from tests.serverrest.ui.pages.login_page import LoginPage
from tests.serverrest.ui.pages.register_page import RegisterPage


class TestLogin:

    @pytest.mark.ui
    def test_login_page_loads(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Verify that the login page loads with all expected elements."""
        login_page = LoginPage(page, serverrest_config)
        login_page.open()
        login_page.expect_page_loaded()

    @pytest.mark.ui
    def test_login_with_unregistered_user(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Try to login with an unregistered user and verify the error message."""
        login_page = LoginPage(page, serverrest_config)
        login_page.open()
        login_page.login("unregistered@example.com", "teste123")
        login_page.expect_login_error()

    @pytest.mark.ui
    def test_navigate_and_register(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Navigate to register page and register a new user."""
        email = "john.doe@email.com"
        register_page = RegisterPage(page, serverrest_config)
        try:
            register_page.open()
            register_page.register("John Doe", email, "password123")
            register_page.expect_success()
        finally:
            delete_user_by_email(serverrest_config, email)

    @pytest.mark.ui
    def test_login_with_registered_user(self, page: Page, serverrest_config: ServerRestConfig, registered_user) -> None:
        """Create user via API, then login via UI and verify the home page."""
        login_page = LoginPage(page, serverrest_config)
        login_page.open()
        login_page.login(registered_user["email"], registered_user["password"])
        login_page.expect_logged_in(registered_user["nome"])