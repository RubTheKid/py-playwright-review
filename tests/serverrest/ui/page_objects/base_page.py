from __future__ import annotations

from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Base Page Object com métodos comuns para todas as páginas."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = "") -> None:
        """Navega para uma URL (relativa ao base_url ou absoluta)."""
        if path.startswith("http"):
            self.page.goto(path)
        else:
            url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
            self.page.goto(url)

    def input(self, selector: str, value: str, clear_first: bool = True) -> None:
        """Preenche um input field."""
        locator = self.page.locator(selector)
        if clear_first:
            locator.clear()
        locator.fill(value)

    def click(self, selector: str) -> None:
        """Clica em um elemento."""
        self.page.locator(selector).click()

    def get_text(self, selector: str) -> str:
        """Retorna o texto de um elemento."""
        return self.page.locator(selector).text_content() or ""

    def is_visible(self, selector: str) -> bool:
        """Verifica se um elemento está visível."""
        return self.page.locator(selector).is_visible()

    def wait_for_selector(self, selector: str, timeout: int = 30000) -> Locator:
        """Aguarda um elemento aparecer."""
        return self.page.wait_for_selector(selector, timeout=timeout)

    def expect_title(self, title: str) -> None:
        """Verifica o título da página."""
        expect(self.page).to_have_title(title)

    def expect_url(self, url_pattern: str) -> None:
        """Verifica a URL atual."""
        expect(self.page).to_have_url(url_pattern)

    def get_locator(self, selector: str) -> Locator:
        """Retorna um Locator para uso avançado."""
        return self.page.locator(selector)

