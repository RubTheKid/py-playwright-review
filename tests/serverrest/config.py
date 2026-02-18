from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class ServerRestConfig:
    ui_base_url: str
    api_base_url: str


def load_serverrest_config() -> ServerRestConfig:
    ui_base_url = os.getenv("SERVERREST_UI_BASE_URL")
    api_base_url = os.getenv("SERVERREST_API_BASE_URL")
    return ServerRestConfig(ui_base_url=ui_base_url, api_base_url=api_base_url)