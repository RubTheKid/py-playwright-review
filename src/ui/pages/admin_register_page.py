from src.ui.pages.base_page import BasePage
from playwright.sync_api import expect

class AdminRegisterPage(BasePage):
    def open(self) -> None:
        self.page.locator('a[data-testid="cadastrarUsuarios"]').click()

    def register(self, nome: str, email: str, password: str, administrador: str = "false") -> None:
        self.page.locator('input[data-testid="nome"]').fill(nome)
        self.page.locator('input[data-testid="email"]').fill(email)
        self.page.locator('input[data-testid="password"]').fill(password)

        admin_locator = self.page.locator('input[data-testid="administrador"]')
        if admin_locator.count() > 0:
            admin_locator.first.check() if administrador == "true" else admin_locator.first.uncheck()

        self.page.locator('button[data-testid="cadastrarUsuario"]').click()

    def expect_user_in_list(self, email: str, nome: str, password: str) -> None:
        self.wait_for_url("/admin/listarusuarios")
        row = self.page.locator('table.table.table-striped').locator(f'tr:has(td:text("{email}"))')
        expect(row).to_be_visible()
        expect(row.locator(f'td:text("{nome}")')).to_be_visible()
        expect(row.locator(f'td:text("{password}")')).to_be_visible()