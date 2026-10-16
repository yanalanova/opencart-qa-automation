from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "index.php?route=account/login"
    LOGOUT_PATH = "index.php?route=account/logout"

    def __init__(self, page):
        super().__init__(page)

        self.email_input = page.locator("#input-email")
        self.password_input = page.locator("#input-password")
        self.login_button = page.get_by_role("button", name="Вхід")
        self.wrong_credentials_alert = page.locator(".alert-danger")

    def open(self):
        super().open(self.PATH)

    def login(self, email, password):
        """Вводить email і пароль та надсилає форму логіну."""
        self.email_input.fill(email)
        self.password_input.fill(password)

        with self.page.expect_navigation():
            self.login_button.click()

    def logout(self):
        """Виходить з акаунту через прямий маршрут логауту."""
        super().open(self.LOGOUT_PATH)
