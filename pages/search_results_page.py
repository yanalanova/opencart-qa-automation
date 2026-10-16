from pages.base_page import BasePage


NO_RESULTS_TEXT = "Немає продуктів які б відповідали критеріям пошуку."


class SearchResultsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.product_cards = page.locator(".product-thumb")
        self.no_results_message = page.get_by_text(
            NO_RESULTS_TEXT,
            exact=True,
        )

    def card_link(self, index):
        """Повертає посилання з назвою товару за індексом картки."""
        return self.product_cards.nth(index).locator("h4 a")

    def card_names(self):
        """Повертає список назв знайдених товарів."""
        names = []

        for index in range(self.product_cards.count()):
            name = self.card_link(index).inner_text().strip()
            names.append(name)

        return names