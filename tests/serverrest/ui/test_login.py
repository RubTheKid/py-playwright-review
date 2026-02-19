import pytest
from tests.serverrest.config import ServerRestConfig 
from playwright.sync_api import Page, expect

from tests.serverrest.api.helpers.api_helpers import delete_user_by_email
from tests.serverrest.ui.helpers.ui_helpers import (
    fill_login_form,
    fill_register_form,
    go_to_login,
    open_register_page,
    expect_register_success,
    expect_user_logged_in,
    expect_login_error,
    expect_login_page_loaded,
)

class TestLogin:

    @pytest.mark.ui
    def test_login_page_loads(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Go to login page and verify if the elements are visible."""
        go_to_login(page, serverrest_config)
        expect_login_page_loaded(page)

    @pytest.mark.ui 
    def test_login_with_unregistered_user(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Try to login with an unregistered user and verify if the error message is visible."""
        go_to_login(page, serverrest_config)
        fill_login_form(page, "unregistered@example.com", "teste123")
        expect_login_error(page)

    @pytest.mark.ui
    def test_navigate_and_register(self, page: Page, serverrest_config: ServerRestConfig) -> None:
        """Go to register page and register a new user."""
        
        email = "john.doe@email.com"
        name = "John Doe"
        password = "password123"

        try:
            go_to_login(page, serverrest_config)
            open_register_page(page)
            fill_register_form(page, name, email, password)
            expect_register_success(page)
        finally:
            delete_user_by_email(serverrest_config, email)

    @pytest.mark.ui
    def test_login_with_registered_user(self, page: Page, serverrest_config: ServerRestConfig, registered_user) -> None:
        """Create user via API, then login in UI."""
        go_to_login(page, serverrest_config)
        fill_login_form(page, registered_user["email"], registered_user["password"])
        expect_user_logged_in(page, registered_user["nome"])