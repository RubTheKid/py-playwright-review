import pytest
from playwright.sync_api import Page

from src.config import ServerRestConfig
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