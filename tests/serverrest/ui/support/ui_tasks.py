from playwright.sync_api import Page
from tests.serverrest.config import ServerRestConfig
from tests.serverrest.ui.pages.login_page import LoginPage
from tests.serverrest.ui.pages.register_page import RegisterPage
from tests.serverrest.ui.pages.admin_register_page import AdminRegisterPage


def login_as(page: Page, config: ServerRestConfig, email: str, password: str) -> None:
    """Complete login flow: open page, fill form."""
    login_page = LoginPage(page, config)
    login_page.open()
    login_page.login(email, password)


def register_user_via_ui(page: Page, config: ServerRestConfig, nome: str, email: str, password: str) -> None:
    """Complete public registration flow."""
    register_page = RegisterPage(page, config)
    register_page.open()
    register_page.register(nome, email, password)
    register_page.expect_success()


def admin_register_user(page: Page, config: ServerRestConfig, nome: str, email: str, password: str) -> None:
    """Complete admin registration flow: open dashboard form, fill and submit."""
    admin_register = AdminRegisterPage(page, config)
    admin_register.open()
    admin_register.register(nome, email, password, "true")