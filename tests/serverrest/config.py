from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class ServerRestConfig:
    UI_BASE_URL: str
    API_BASE_URL: str


def load_serverrest_config() -> ServerRestConfig:
    UI_BASE_URL = os.getenv("SERVERREST_UI_BASE_URL")
    API_BASE_URL = os.getenv("SERVERREST_API_BASE_URL")
    return ServerRestConfig(UI_BASE_URL=UI_BASE_URL, API_BASE_URL=API_BASE_URL)