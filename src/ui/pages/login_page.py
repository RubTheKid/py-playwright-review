from playwright.sync_api import Page, Locator, expect
from src.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object Model for Front - ServeRest @page /login"""

    CONFIG = {
        'PAGE_PATH': '/login',
        'TIMEOUTS': {
            'PAGE_LOAD': 10000,
            'ELEMENT_VISIBLE': 2000,
            'NAVIGATION': 30000
        }
    }

    def __init__(self, page: Page, config) -> None:
        super().__init__(page, config)

    @property
    def email_input(self) -> Locator:
        return self.page.locator('input[data-testid="email"]')

    @property
    def password_input(self) -> Locator:
        return self.page.locator('input[data-testid="senha"]')

    @property
    def login_button(self) -> Locator:
        return self.page.locator('button[data-testid="entrar"]')

    @property
    def error_message(self) -> Locator:
        return self.page.locator('div.alert.alert-secondary')

    @property
    def register_link(self) -> Locator:
        return self.page.locator('a[data-testid="cadastrar"]')

    def open(self) -> None:
        self.goto(self.CONFIG['PAGE_PATH'])

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_page_loaded(self) -> None:
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()

    def expect_login_error(self) -> None:
        expect(self.error_message).to_be_visible(timeout=5000)

    def expect_logged_in(self, nome: str) -> None:
        expect(self.page.locator(f'.jumbotron h1:has-text("{nome}")')).to_be_visible()
