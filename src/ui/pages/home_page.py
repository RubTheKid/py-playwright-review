from playwright.sync_api import Page, Locator, expect

from src.ui.pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object Model for Front - ServeRest @page /home"""

    CONFIG = {
        'PAGE_PATH': '/home',
        'TIMEOUTS': {
            'PAGE_LOAD': 10000,
            'ELEMENT_VISIBLE': 2000,
            'NAVIGATION': 30000
        }
    }

    def __init__(self, page: Page, config) -> None:
        super().__init__(page, config)

    # Navigation elements

    @property
    def home_link(self) -> Locator:
        return self.page.get_by_test_id('home')

    @property
    def lista_de_compras_link(self) -> Locator:
        return self.page.get_by_test_id('lista-de-compras')

    @property
    def carrinho_link(self) -> Locator:
        return self.page.get_by_test_id('carrinho')

    @property
    def logout_button(self) -> Locator:
        return self.page.get_by_test_id('logout')

    @property
    def search_input(self) -> Locator:
        return self.page.get_by_test_id('pesquisar')

    @property
    def pesquisar_button(self) -> Locator:
        return self.page.get_by_test_id('botaoPesquisar')

    # Product list (cards)

    @property
    def product_cards(self) -> Locator:
        """All product cards in the grid."""
        return self.page.locator('.card.col-3')

    def product_card_by_name(self, name: str) -> Locator:
        """Single product card containing the given product name."""
        return self.product_cards.filter(has_text=name)

    def product_card_at(self, index: int) -> Locator:
        """Product card at zero-based index."""
        return self.product_cards.nth(index)

    def add_to_list_button_in_card(self, card: Locator) -> Locator:
        """'Adicionar a lista' button scoped to a specific card."""
        return card.get_by_test_id('adicionarNaLista')

    def detail_link_in_card(self, card: Locator) -> Locator:
        """'Detalhes' link scoped to a specific card."""
        return card.locator('a.card-link')

    def open(self) -> None:
        self.goto(self.CONFIG['PAGE_PATH'])

    def expect_product_cards_visible(self, min_count: int = 1) -> None:
        """Assert that at least min_count product cards are visible."""
        expect(self.product_cards.first).to_be_visible(timeout=5000)
        assert self.product_cards.count() >= min_count

    def expect_product_in_list(self, name: str, price: str | None = None) -> None:
        """Assert that a product with given name (and optionally price) is in the list."""
        card = self.product_card_by_name(name)
        expect(card).to_be_visible()
        expect(card.locator('.card-title')).to_contain_text(name)
        if price:
            expect(card).to_contain_text(price)

