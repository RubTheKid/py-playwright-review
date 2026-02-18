import pytest

from tests.serverrest.config import ServerRestConfig
from tests.serverrest.fixtures.config import serverrest_config as _serverrest_config


@pytest.fixture(scope="session")
def serverrest_config() -> ServerRestConfig:
    """Configuração do ServeRest (UI e API base URLs)."""
    return _serverrest_config()


