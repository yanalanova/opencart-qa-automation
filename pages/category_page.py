# pages/category_page.py
from pages.base_page import BasePage
import re



class CategoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.heading = page.locator("h2")
        self.products = page.locator(".product-thumb")
        self.breadcrumb = page.locator("ul.breadcrumb")
        self.breadcrumb_home = self.breadcrumb.locator("li").first.locator("a")
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
        self.breadcrumb.get_by_role(
            "link",
            name=name,
            exact=True,
        ).click()
