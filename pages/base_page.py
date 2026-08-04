from config import BASE_URL


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, path=""):
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url)
