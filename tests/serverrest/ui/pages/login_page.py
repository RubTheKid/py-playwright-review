from playwright.sync_api import expect
from tests.serverrest.ui.pages.base_page import BasePage

class LoginPage(BasePage):

    def open(self) -> None:
        self.goto("/login")

    def login(self, email: str, password: str) -> None:
        self.page.locator('input[data-testid="email"]').fill(email)
        self.page.locator('input[data-testid="senha"]').fill(password)
        self.page.locator('button[data-testid="entrar"]').click()

    def expect_page_loaded(self) -> None:
        expect(self.page.locator('input[data-testid="email"]')).to_be_visible()
        expect(self.page.locator('input[data-testid="senha"]')).to_be_visible()
        expect(self.page.locator('button[data-testid="entrar"]')).to_be_visible()

    def expect_login_error(self) -> None:
        expect(self.page.locator('div.alert.alert-secondary')).to_be_visible(timeout=5000)

    def expect_logged_in(self, nome: str) -> None:
        expect(self.page.locator(f'.jumbotron h1:has-text("{nome}")')).to_be_visible()