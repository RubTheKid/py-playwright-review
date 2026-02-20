from src.ui.pages.base_page import BasePage
from playwright.sync_api import expect

class AdminListProductPage(BasePage):
    def open(self) -> None:
        self.wait_for_url("/admin/listarprodutos")

    def expect_product_in_list(self, name: str, price: str, description: str, quantity: str) -> None:
        self.wait_for_url("/admin/listarprodutos")
        row = self.page.locator('table.table.table-striped').locator(f'tr:has(td:text-is("{name}"))')
        expect(row).to_be_visible()
        expect(row.locator(f'td:text-is("{name}")')).to_be_visible()
        expect(row.locator(f'td:text-is("{price}")')).to_be_visible()
        expect(row.locator(f'td:text-is("{description}")')).to_be_visible()
        expect(row.locator(f'td:text-is("{quantity}")')).to_be_visible()