import pytest

from tests.serverrest.config import ServerRestConfig, load_serverrest_config


@pytest.fixture(scope="session")
def serverrest_config() -> ServerRestConfig:
    """Configuração do ServeRest (UI e API base URLs)."""
    return load_serverrest_config()