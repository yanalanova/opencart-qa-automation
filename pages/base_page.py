from config import BASE_URL
import re


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, path=""):
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url)

    def cart_count(self):
        """Повертає кількість товарів у кошику."""
        cart_text = self.page.locator("#cart-total").inner_text()
        match = re.search(r"\d+", cart_text)
        return int(match.group()) if match else 0
