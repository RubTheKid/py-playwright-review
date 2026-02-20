from playwright.sync_api import Page
from src.config import ServerRestConfig

class BasePage:
    def __init__(self, page: Page, config: ServerRestConfig) -> None:
        self.page = page
        self.config = config

    def goto(self, path: str) -> None:
        self.page.goto(f"{self.config.UI_BASE_URL}{path}")

    def wait_for_url(self, path: str) -> None:
        self.page.wait_for_url(f"{self.config.UI_BASE_URL}{path}")