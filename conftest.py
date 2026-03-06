import pytest
from playwright.sync_api import Page

from src.config import ServerRestConfig, load_serverrest_config
from src.api.helpers.api_helpers import delete_user_by_email, create_user
from src.api.helpers.api_helpers import login_admin, delete_product_by_nome
from src.ui.pages.login_page import LoginPage
from src.ui.pages.home_page import HomePage


@pytest.fixture(scope="session")
def serverrest_config() -> ServerRestConfig:
    """serverest config (UI e API base URLs)."""
    return load_serverrest_config()


@pytest.fixture
def register_admin_user(serverrest_config: ServerRestConfig):
    """Setup: create admin user via API. Teardown: delete user after test."""
    email = "testerava@email.com"
    password = "teste123"
    nome = "Ava Test"

    delete_user_by_email(serverrest_config, email)
    user_id = create_user(serverrest_config, email, password, nome, administrador="true")

    yield {"email": email, "password": password, "nome": nome, "id": user_id}

    delete_user_by_email(serverrest_config, email)


@pytest.fixture
def logged_in_home(page: Page, serverrest_config: ServerRestConfig):
    """Create user, login via UI, and yield HomePage (already on /home)."""
    email = "producttest@email.com"
    password = "teste123"
    nome = "Product Test User"

    delete_user_by_email(serverrest_config, email)
    create_user(serverrest_config, email, password, nome, administrador="false")

    try:
        login_page = LoginPage(page, serverrest_config)
        login_page.open()
        login_page.login(email, password)
        page.wait_for_url("**/home**", timeout=10000)
        home_page = HomePage(page, serverrest_config)
        home_page.open()
        yield home_page
    finally:
        delete_user_by_email(serverrest_config, email)

@pytest.fixture
def registered_product(serverrest_config: ServerRestConfig, register_admin_user):
    """Setup: delete 'Product 1' if leftover from previous run. Teardown: delete after test."""
    nome = "Product 1"
    token = login_admin(serverrest_config, register_admin_user["email"], register_admin_user["password"])

    # setup
    delete_product_by_nome(serverrest_config, token, nome)

    yield {"nome": nome, "token": token}

    # teardown
    delete_product_by_nome(serverrest_config, token, nome)
