import pytest

from src.ui.pages.home_page import HomePage

class TestProductList:
    @pytest.mark.ui
    def test_product_list_displays_cards(self, logged_in_home: HomePage) -> None:
        """Verify that the product list shows at least one product card."""
        logged_in_home.expect_product_cards_visible(min_count=1)

    @pytest.mark.ui
    def test_product_list_has_multiple_cards(self, logged_in_home: HomePage) -> None:
        """Verify that multiple product cards are displayed."""
        count = logged_in_home.product_cards.count()
        assert count >= 1, "Expected at least 1 product card"

    @pytest.mark.ui
    def test_find_product_by_name_and_verify_price(
        self, logged_in_home: HomePage
    ) -> None:
        """Find a product by name and verify it shows a price."""
        # Get the first card's title to use as search target
        first_card = logged_in_home.product_card_at(0)
        product_name = first_card.locator(".card-title").text_content()
        assert product_name, "Product card should have a title"

        product_name = product_name.strip()
        logged_in_home.expect_product_in_list(product_name)

    @pytest.mark.ui
    def test_add_to_list_button_exists_in_each_card(
        self, logged_in_home: HomePage
    ) -> None:
        """Verify each product card has an 'Adicionar a lista' button."""
        cards = logged_in_home.product_cards
        count = cards.count()
        assert count >= 1, "Expected at least 1 product card"

        for i in range(count):
            card = logged_in_home.product_card_at(i)
            add_btn = logged_in_home.add_to_list_button_in_card(card)
            add_btn.wait_for(state="visible", timeout=2000)
