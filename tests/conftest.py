import pytest

from tests.serverrest.config import ServerRestConfig, load_serverrest_config
from tests.serverrest.support.api_tasks import delete_user_by_email, create_user  

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