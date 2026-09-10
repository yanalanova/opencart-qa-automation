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

    def card_link(self, index):
        """Return the product link from a card."""
        return self.card(index).locator("h4 a")

    def card_price(self, index):
        """Return the product price from a card."""
        return self.card(index).locator(".price")

    def card_add_button(self, index):
        """Return the Add to Cart button from a card."""
        return self.card(index).locator("button[onclick^='cart.add']")

    def card_name_link(self, card):
        """Return the product link from a specific card locator."""
        return card.locator("h4 a")

    def card_add_button_by_card(self, card):
        """Return the Add to Cart button from a specific card locator."""
        return card.locator("button[onclick^='cart.add']")

    def card_wishlist_button(self, index):
        """Return the Add to Wishlist button from a card."""
        return self.card(index).locator("button[onclick*='wishlist.add']")

    def card_wishlist_button_by_card(self, card):
        """Return the Add to Wishlist button from a specific card locator."""
        return card.locator("button[onclick*='wishlist.add']")

    def get_product_info(self, index):
        """Get product information from a card by index.

        Returns a dictionary with:
            - name: Product name text
            - href: Product URL link
            - price: Product price text
            - add_button: Add to Cart button locator
            - wishlist_button: Add to Wishlist button locator
        """
        return {
            "name": self.card_link(index).inner_text().strip(),
            "href": self.card_link(index).get_attribute("href"),
            "price": self.card_price(index).inner_text().strip(),
            "add_button": self.card_add_button(index),
            "wishlist_button": self.card_wishlist_button(index),
        }

    def get_product_info_by_card(self, card):
        """Get product information from a specific card locator.

        Returns a dictionary with:
            - name: Product name text
            - href: Product URL link
            - price: Product price text
            - add_button: Add to Cart button locator
            - wishlist_button: Add to Wishlist button locator
        """
        return {
            "name": self.card_name_link(card).inner_text().strip(),
            "href": self.card_name_link(card).get_attribute("href"),
            "price": card.locator(".price").inner_text().strip(),
            "add_button": self.card_add_button_by_card(card),
            "wishlist_button": self.card_wishlist_button_by_card(card),
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
        
