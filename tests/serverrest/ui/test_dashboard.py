import pytest
from playwright.sync_api import Page

from tests.serverrest.config import ServerRestConfig
from tests.serverrest.api.helpers.api_helpers import delete_user_by_email
from tests.serverrest.ui.helpers.ui_helpers import (
    go_to_login,
    fill_login_form,
    fill_register_form,
    expect_user_logged_in,
    open_admin_register_page,
    expect_user_in_list,
    fill_admin_register_form,
)


class TestDashboard:

    @pytest.mark.ui
    def test_admin_register_user_and_verify_in_list(
        self,
        page: Page,
        serverrest_config: ServerRestConfig,
        registered_user: dict,
    ) -> None:
        """Login as admin, register a new user in dashboard, verify in user list."""

        new_name = "John Sylva"
        new_email = "john.sylva@email.com"
        new_password = "senha123"

        try:
            go_to_login(page, serverrest_config)
            fill_login_form(page, registered_user["email"], registered_user["password"])
            expect_user_logged_in(page, registered_user["nome"])
            open_admin_register_page(page)
            fill_admin_register_form(page, new_name, new_email, new_password, "true")
            expect_user_in_list(page, serverrest_config, new_email, new_name, new_password)
        finally:
            delete_user_by_email(serverrest_config, new_email)