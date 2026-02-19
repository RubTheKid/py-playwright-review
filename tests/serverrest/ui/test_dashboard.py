import pytest
from playwright.sync_api import Page

from tests.serverrest.config import ServerRestConfig
from tests.serverrest.api.helpers.api_helpers import delete_user_by_email
from tests.serverrest.ui.pages.login_page import LoginPage
from tests.serverrest.ui.pages.admin_register_page import AdminRegisterPage
from tests.serverrest.ui.pages.admin_register_product import AdminRegisterProductPage
from tests.serverrest.ui.pages.admin_list_product import AdminListProductPage


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
            login_page = LoginPage(page, serverrest_config)
            login_page.open()
            login_page.login(registered_user["email"], registered_user["password"])
            login_page.expect_logged_in(registered_user["nome"])

            admin_register = AdminRegisterPage(page, serverrest_config)
            admin_register.open()
            admin_register.register(new_name, new_email, new_password, "true")
            admin_register.expect_user_in_list(new_email, new_name, new_password)
        finally:
            delete_user_by_email(serverrest_config, new_email)

    @pytest.mark.ui
    def test_admin_register_product_and_verify_in_list(
        self,
        page: Page,
        serverrest_config: ServerRestConfig,
        registered_user: dict,
        registered_product: dict,
    ) -> None:
        """Login as admin, register a new product in dashboard, verify in product list."""

        new_product_name = "Product 1"
        new_product_price = "100"
        new_product_description = "Product 1 description"
        new_product_quantity = "10"

        login_page = LoginPage(page, serverrest_config)
        login_page.open()
        login_page.login(registered_user["email"], registered_user["password"])
        login_page.expect_logged_in(registered_user["nome"])

        admin_register_product = AdminRegisterProductPage(page, serverrest_config)
        admin_register_product.open()
        admin_register_product.register(new_product_name, new_product_price, new_product_description, new_product_quantity)

        admin_list_product = AdminListProductPage(page, serverrest_config)
        admin_list_product.expect_product_in_list(new_product_name, new_product_price, new_product_description, new_product_quantity)