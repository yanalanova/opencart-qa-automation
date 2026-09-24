# pages/category_page.py
from pages.base_page import BasePage
import re


class CategoryPage(BasePage):
    PATH = "desktops"

    def __init__(self, page):
        super().__init__(page)

        self.heading = page.locator("h2")
        self.products = page.locator(".product-thumb")
        self.breadcrumb = page.locator("ul.breadcrumb")
        self.breadcrumb_home = self.breadcrumb.locator("li").first.locator("a")

        # Header and alerts
        self.header_cart = page.locator("#cart-total")
        self.success_alert = page.locator(".alert-success")

    def open(self):
        """Open the category page."""
        super().open(self.PATH)

    def card_by_text(self, text):
        """Return a product card by text."""
        return self.products.filter(has_text=text)

    def card(self, index):
        """Return a product card by index."""
        return self.products.nth(index)

    def card_link(self, card):
        """Return the product link from a card."""
        return card.locator("h4 a")

    def card_price(self, card):
        """Return the product price from a card."""
        return card.locator(".price")

    def card_add_button(self, card):
        """Return the Add to Cart button from a card."""
        return card.locator("button[onclick^='cart.add']")

    def card_wishlist_button(self, card):
        """Return the Add to Wishlist button from a card."""
        return card.locator("button[onclick*='wishlist.add']")

    def get_product_info(self, card):
        """Get product data from a card locator.

        Returns a dictionary with:
            - name: Product name text
            - href: Product URL link
            - price: Product price text
        """
        link = self.card_link(card)

        return {
            "name": link.inner_text().strip(),
            "href": link.get_attribute("href"),
            "price": self.card_price(card).inner_text().strip(),
        }

    def subcategory_link(self, name):
        
        # Знаходить посилання підкатегорії, наприклад "Mac (1)"
        return self.page.locator("#content").get_by_role(
            "link",
            name=re.compile(rf"^{re.escape(name)}\s*\(\d+\)$"),
        )

    def open_subcategory(self, name):
        # Відкриває вибрану підкатегорію
        self.subcategory_link(name).click()

    def click_breadcrumb(self, name):
        # Переходить на вибраний рівень через breadcrumb
        self.breadcrumb.get_by_role("link",name=name,exact=True,).click()
        
