from config import BASE_URL
import re


class BasePage:
    def __init__(self, page):
        self.page = page

        # Search поле та кнопка — є в шапці кожної сторінки
        self.search_input = page.locator("div#search input[name='search']")
        self.search_button = page.locator("div#search button")

    def open(self, path=""):
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url)

    def search(self, term):
        """Ввести пошуковий запит і натиснути кнопку пошуку."""
        self.search_input.fill(term)
        self.search_button.click()

    def cart_count(self):
        """Повертає кількість товарів у кошику."""
        cart_text = self.page.locator("#cart-total").inner_text()
        match = re.search(r"\d+", cart_text)
        return int(match.group()) if match else 0
