from tests.serverrest.ui.pages.base_page import BasePage
from playwright.sync_api import expect

class AdminRegisterProductPage(BasePage):
    def open(self) -> None:
        self.page.locator('a[data-testid="cadastrarProdutos"]').click()

    
    def register(self, name: str, price: float, description: str, quantity: int) -> None:
        self.page.locator('input[data-testid="nome"]').fill(name)
        self.page.locator('input[data-testid="preco"]').fill(price)
        self.page.locator('textarea[data-testid="descricao"]').fill(description)
        self.page.locator('input[data-testid="quantity"]').fill(quantity)

        self.page.locator('button[data-testid="cadastarProdutos"]').click()