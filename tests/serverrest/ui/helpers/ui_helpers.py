from playwright.sync_api import Page, expect

from tests.serverrest.config import ServerRestConfig

def expect_login_page_loaded(page: Page) -> None:
    expect(page.locator('input[data-testid="email"]')).to_be_visible()
    expect(page.locator('input[data-testid="senha"]')).to_be_visible()
    expect(page.locator('button[data-testid="entrar"]')).to_be_visible()

def fill_login_form(page: Page, email: str, password: str) -> None:
    """Fill and submit the login form."""
    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="senha"]').fill(password)
    page.locator('button[data-testid="entrar"]').click()

def fill_register_form(page: Page, nome: str, email: str, password: str, administrador: str = "false") -> None:
    """Fill and submit the registration form."""
    page.locator('input[data-testid="nome"]').fill(nome)
    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="password"]').fill(password)

    admin_locator = page.locator(
        'input[data-testid="administrador"], input[name="administrador"], input#administrador'
    )
    if admin_locator.count() > 0:
        if str(administrador).lower() == "true":
            admin_locator.first.check()
        else:
            admin_locator.first.uncheck()

    page.locator('button[data-testid="cadastrar"]').click()

def go_to_login(page: Page, config: ServerRestConfig) -> None:
    page.goto(f"{config.UI_BASE_URL}/login")

def open_register_page(page: Page) -> None:
    page.locator('a[data-testid="cadastrar"]').click()

def expect_login_error(page: Page) -> None:
    expect(page.locator('div.alert.alert-secondary')).to_be_visible(timeout=5000)

def expect_register_success(page: Page) -> None:
    expect(page.locator('div.alert.alert-primary')).to_be_visible()

def expect_user_logged_in(page: Page, nome: str) -> None:
    expect(page.locator(f'.jumbotron h1:has-text("{nome}")')).to_be_visible()

def open_admin_register_page(page: Page) -> None:
    """Click register user link in the admin dashboard"""
    page.locator('a[data-testid="cadastrarUsuarios"]').click()

def expect_user_in_list(page: Page, config: ServerRestConfig, email: str, nome: str, password: str) -> None:
    """Verify that a user appears in the admin user list table"""
    expect(page).to_have_url(f"{config.UI_BASE_URL}/admin/listarusuarios")
    row = page.locator('table.table.table-striped').locator(f'tr:has(td:text("{email}"))')
    expect(row).to_be_visible()
    expect(row.locator(f'td:text("{nome}")')).to_be_visible()
    expect(row.locator(f'td:text("{password}")')).to_be_visible()


def fill_admin_register_form(page: Page, nome: str, email: str, password: str, administrador: str = "false") -> None:
    """Fill and submit the user registration form from the admin dashboard."""
    page.locator('input[data-testid="nome"]').fill(nome)
    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="password"]').fill(password)

    admin_locator = page.locator(
        'input[data-testid="administrador"], input[name="administrador"], input#administrador'
    )
    if admin_locator.count() > 0:
        if str(administrador).lower() == "true":
            admin_locator.first.check()
        else:
            admin_locator.first.uncheck()

    page.locator('button[data-testid="cadastrarUsuario"]').click()