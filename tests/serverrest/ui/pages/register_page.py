from playwright.sync_api import expect
from tests.serverrest.ui.pages.base_page import BasePage

class RegisterPage(BasePage):
    def open(self) -> None:
        self.goto("/login")
        self.page.locator('a[data-testid="cadastrar"]').click()

    def register(self, nome: str, email: str, password: str) -> None:
        self.page.locator('input[data-testid="nome"]').fill(nome)
        self.page.locator('input[data-testid="email"]').fill(email)
        self.page.locator('input[data-testid="password"]').fill(password)
        self.page.locator('button[data-testid="cadastrar"]').click()

    def expect_success(self) -> None:
        expect(self.page.locator('div.alert.alert-primary')).to_be_visible()