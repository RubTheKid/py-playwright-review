import pytest

from src.config import ServerRestConfig, load_serverrest_config
from src.api.helpers.api_helpers import delete_user_by_email, create_user
from src.api.helpers.api_helpers import login_admin, delete_product_by_nome

@pytest.fixture(scope="session")
def serverrest_config() -> ServerRestConfig:
    """Configuração do ServeRest (UI e API base URLs)."""
    return load_serverrest_config()

@pytest.fixture
def registered_user(serverrest_config: ServerRestConfig):
    """Setup: create user via API. Teardown: delete user via API after test."""
    email = "testerava@email.com"
    password = "teste123"
    nome = "Ava Test"

    # setup
    delete_user_by_email(serverrest_config, email)
    user_id = create_user(serverrest_config, email, password, nome, administrador="true")

    yield {"email": email, "password": password, "nome": nome, "id": user_id}

    # teardown
    delete_user_by_email(serverrest_config, email)

@pytest.fixture
def registered_product(serverrest_config: ServerRestConfig, registered_user):
    """Setup: delete 'Product 1' if leftover from previous run. Teardown: delete after test."""
    nome = "Product 1"
    token = login_admin(serverrest_config, registered_user["email"], registered_user["password"])

    # setup
    delete_product_by_nome(serverrest_config, token, nome)

    yield {"nome": nome, "token": token}

    # teardown
    delete_product_by_nome(serverrest_config, token, nome)
