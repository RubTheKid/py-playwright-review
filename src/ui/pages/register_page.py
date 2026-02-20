# from playwright.sync_api import expect
# from src.ui.pages.base_page import BasePage

# class RegisterPage(BasePage):
#     def open(self) -> None:
#         self.goto("/login")
#         self.page.locator('a[data-testid="cadastrar"]').click()

#     def register(self, nome: str, email: str, password: str) -> None:
#         self.page.locator('input[data-testid="nome"]').fill(nome)
#         self.page.locator('input[data-testid="email"]').fill(email)
#         self.page.locator('input[data-testid="password"]').fill(password)
#         self.page.locator('button[data-testid="cadastrar"]').click()

#     def expect_success(self) -> None:
#         expect(self.page.locator('div.alert.alert-primary')).to_be_visible()

from playwright.sync_api import Page, Locator, expect
from src.ui.pages.base_page import BasePage

class RegisterPage(BasePage):
    """Page Object Model for Front - ServeRest @page /cadastrarusuarios"""

    CONFIG = {
        'PAGE_PATH': '/cadastrarusuarios',
        'TIMEOUTS': {
            'PAGE_LOAD': 10000,
            'ELEMENT_VISIBLE': 2000,
            'NAVIGATION': 30000
        }
    }
    
    def __init__(self, page: Page, config) -> None:
        super().__init__(page, config)

    def open(self) -> None:
        self.goto(self.CONFIG['PAGE_PATH'])

    def register(self, name: str, email: str, password: str) -> None:
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.register_button.click()

    def expect_page_loaded(self) -> None:
        expect(self.name_input).to_be_visible()
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.register_button).to_be_visible()

    def expect_error_messages(self) -> None:
        expect(self.error_name_required).to_be_visible()
        expect(self.error_email_required).to_be_visible()
        expect(self.error_password_required).to_be_visible()

    # inputs
    @property
    def name_input(self) -> Locator:
        return self.page.locator('input[data-testid="nome"]')

    @property
    def email_input(self) -> Locator:
        return self.page.locator('input[data-testid="email"]')

    @property
    def password_input(self) -> Locator:
        return self.page.locator('input[data-testid="password"]')

    @property
    def admin_checkbox(self) -> Locator:
        return self.page.locator('input[id="administrador"]')

    @property
    def return_to_login_link(self) -> Locator:
        return self.page.locator('a[data-testid="entrar"]')


    # buttons
    @property
    def register_button(self) -> Locator:
        return self.page.locator('button[data-testid="cadastrar"]')

    # messages
    @property
    def success_message(self) -> Locator:
        return self.page.locator('div.alert.alert-primary')


    # errors
    @property
    def error_name_required(self) -> Locator:
        return self.page.locator(
            'div.alert.alert-secondary.alert-dismissible span:text-is("Nome é obrigatório")'
        ).first

    @property
    def error_email_required(self) -> Locator:
        return self.page.locator(
            'div.alert.alert-secondary.alert-dismissible span:text-is("Email é obrigatório")'
        ).first

    @property
    def error_password_required(self) -> Locator:
        return self.page.locator(
            'div.alert.alert-secondary.alert-dismissible span:text-is("Password é obrigatório")'
        ).first
