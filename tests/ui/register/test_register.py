import pytest
from playwright.sync_api import Page

from src.config import ServerRestConfig
from src.api.helpers.api_helpers import create_user, delete_user_by_email
from src.ui.pages.login_page import LoginPage
from src.ui.pages.register_page import RegisterPage


class TestRegister:
    @pytest.mark.ui
    def test_register_page_loads(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Verify that the register page loads with all expected elements."""
        register_page = RegisterPage(page, serverrest_config)
        register_page.open()
        register_page.expect_page_loaded()

    @pytest.mark.ui
    def test_register_with_invalid_data(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Try to register with invalid data and verify the error messages."""
        register_page = RegisterPage(page, serverrest_config)
        register_page.open()
        register_page.register("", "", "")
        register_page.expect_error_messages()

    @pytest.mark.ui
    def test_navigate_and_register(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Navigate to register, create new user, verify success (alert or redirect to home)."""
        email = "navregister@qa.com"
        nome = "Navigate Register User"
        password = "teste123"

        delete_user_by_email(serverrest_config, email)

        try:
            # Navigate from login to register
            login_page = LoginPage(page, serverrest_config)
            login_page.open()
            login_page.register_link.click()

            register_page = RegisterPage(page, serverrest_config)
            register_page.register(nome, email, password)
            register_page.expect_success()
        finally:
            delete_user_by_email(serverrest_config, email)