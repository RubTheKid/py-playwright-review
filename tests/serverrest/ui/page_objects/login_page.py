from __future__ import annotations

from playwright.sync_api import Page

from tests.serverrest.ui.page_objects.base_page import BasePage


class LoginPage(BasePage):
    """Page Object para a página de login do ServeRest."""

    # Selectors
    EMAIL_INPUT = 'input[data-testid="email"]'
    PASSWORD_INPUT = 'input[data-testid="senha"]'
    LOGIN_BUTTON = 'button[data-testid="entrar"]'
    REGISTER_BUTTON = 'button[data-testid="cadastrar"]'
    ERROR_MESSAGE = '[data-testid="alerta"]'

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.path = "/login"

    def navigate_to_login(self) -> None:
        """Navega para a página de login."""
        self.navigate(self.path)

    def fill_email(self, email: str) -> None:
        """Preenche o campo de email."""
        self.input(self.EMAIL_INPUT, email)

    def fill_password(self, password: str) -> None:
        """Preenche o campo de senha."""
        self.input(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """Clica no botão de login."""
        self.click(self.LOGIN_BUTTON)

    def click_register(self) -> None:
        """Clica no botão de cadastrar."""
        self.click(self.REGISTER_BUTTON)

    def login(self, email: str, password: str) -> None:
        """Faz login completo."""
        self.fill_email(email)
        self.fill_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Retorna a mensagem de erro, se houver."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

