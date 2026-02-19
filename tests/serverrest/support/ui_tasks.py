from playwright.sync_api import Page

def login(page: Page, email: str, password: str) -> None:
    """Fill and submit the login form."""
    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="senha"]').fill(password)
    page.locator('button[data-testid="entrar"]').click()
    page.wait_for_load_state("networkidle")

def register(page: Page, nome: str, email: str, password: str) -> None:
    """Fill and submit the registration form."""
    page.locator('input[data-testid="nome"]').fill(nome)
    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="password"]').fill(password)
    page.locator('button[data-testid="cadastrar"]').click()
    page.wait_for_load_state("networkidle")

def register_user_as_admin(page: Page, nome: str, email: str, password: str) -> None:
    """Fill and submit the admin user registration form."""
    page.locator('input[data-testid="nome"]').fill(nome)
    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="password"]').fill(password)
    page.locator('button[data-testid="cadastrarUsuario"]').click()
    page.wait_for_load_state("networkidle")