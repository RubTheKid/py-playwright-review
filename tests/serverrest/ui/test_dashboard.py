import pytest
from playwright.sync_api import Page

from tests.serverrest.config import ServerRestConfig
from tests.serverrest.api.helpers.api_helpers import delete_user_by_email
from tests.serverrest.ui.pages.login_page import LoginPage
from tests.serverrest.ui.pages.admin_register_page import AdminRegisterPage
from tests.serverrest.ui.support.ui_tasks import login_as, admin_register_user


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
            login_as(page, serverrest_config, registered_user["email"], registered_user["password"])
            LoginPage(page, serverrest_config).expect_logged_in(registered_user["nome"])

            admin_register_user(page, serverrest_config, new_name, new_email, new_password)
            AdminRegisterPage(page, serverrest_config).expect_user_in_list(new_email, new_name, new_password)
        finally:
            delete_user_by_email(serverrest_config, new_email)