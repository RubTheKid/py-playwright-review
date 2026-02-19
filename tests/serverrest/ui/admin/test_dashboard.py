import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.serverrest.config import ServerRestConfig
from tests.serverrest.support.api_tasks import delete_user_by_email
from tests.serverrest.support.ui_tasks import login, register_user_as_admin

faker = Faker()


@pytest.mark.ui
def test_admin_register_user_and_verify_in_list(
    page: Page,
    serverrest_config: ServerRestConfig,
    registered_user: dict,
) -> None:
    """Login as admin, register a new user in dashboard, verify in user list."""

    new_name = faker.name()
    new_email = faker.email()
    new_password = "senha123"

    page.goto(f"{serverrest_config.UI_BASE_URL}/login")
    login(page, registered_user["email"], registered_user["password"])
    expect(page.locator(f'.jumbotron h1:has-text("{registered_user["nome"]}")')).to_be_visible()

    page.locator('a[data-testid="cadastrarUsuarios"]').click()
    register_user_as_admin(page, new_name, new_email, new_password)

    expect(page).to_have_url(f"{serverrest_config.UI_BASE_URL}/admin/listarusuarios")
    line = page.locator('table.table.table-striped').locator(f'tr:has(td:text("{new_email}"))')
    expect(line).to_be_visible()
    expect(line.locator(f'td:text("{new_name}")')).to_be_visible()
    expect(line.locator(f'td:text("{new_password}")')).to_be_visible()

    delete_user_by_email(serverrest_config, new_email)