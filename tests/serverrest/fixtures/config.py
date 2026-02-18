from tests.serverrest.config import ServerRestConfig, load_serverrest_config


def serverrest_config() -> ServerRestConfig:
    return load_serverrest_config()