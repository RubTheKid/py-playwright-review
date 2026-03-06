import pytest
from playwright.sync_api import Page

from src.config import ServerRestConfig
from src.api.helpers.api_helpers import create_user, delete_user_by_email
from src.ui.pages.login_page import LoginPage
from src.ui.pages.home_page import HomePage

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
    def test_login_with_registered_user(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Register user via API, then login via UI and verify the home page."""
        email = "testerava@email.com"
        password = "teste123"
        nome = "Ava Test"

        delete_user_by_email(serverrest_config, email)
        create_user(serverrest_config, email, password, nome, administrador="false")

        try:
            login_page = LoginPage(page, serverrest_config)
            login_page.open()
            login_page.login(email, password)
            home_page = HomePage(page, serverrest_config)
            home_page.expect_product_cards_visible(min_count=1)
        finally:
            delete_user_by_email(serverrest_config, email)
