from pages.base_page import BasePage


class RegisterPage(BasePage):
    PATH = "index.php?route=account/register"

    def __init__(self, page):
        super().__init__(page)

        self.firstname_input = page.locator("#input-firstname")
        self.lastname_input = page.locator("#input-lastname")
        self.email_input = page.locator("#input-email")
        self.telephone_input = page.locator("#input-telephone")
        self.address_input = page.locator("#input-address-1")
        self.city_input = page.locator("#input-city")
        self.country_select = page.locator("#input-country")
        self.zone_select = page.locator("#input-zone")
        self.password_input = page.locator("#input-password")
        self.confirm_input = page.locator("#input-confirm")
        self.agree_checkbox = page.locator("input[name='agree']")
        self.continue_button = page.get_by_role("button", name="Продовжити")

        self.errors = page.locator(".text-danger")
        self.success_heading = page.locator("h1")
        self.duplicate_email_alert = page.locator(".alert-danger")

    def open(self):
        super().open(self.PATH)

    def fill(self, user):
        """Заповнює всю форму реєстрації даними user, не надсилаючи її."""
        self.firstname_input.fill(user["first_name"])
        self.lastname_input.fill(user["last_name"])
        self.email_input.fill(user["email"])
        self.telephone_input.fill(user["telephone"])
        self.address_input.fill(user["address"])
        self.city_input.fill(user["city"])

        # Сторінка вже має дефолтну країну з підвантаженим списком областей,
        # тому select_option() тут теж запускає AJAX-запит на оновлення списку.
        # Якщо обрати область до того, як ця відповідь прийде, список
        # перезапишеться і скине вибір — тому чекаємо саме цю відповідь.
        with self.page.expect_response(
            lambda response: "route=account/account/country" in response.url
        ):
            self.country_select.select_option(label=user["country"])

        self.zone_select.select_option(label=user["zone"])

        self.password_input.fill(user["password"])
        self.confirm_input.fill(user["password"])
        self.agree_checkbox.check()

    def submit(self):
        """Надсилає форму реєстрації."""
        # Форма повністю перезавантажує сторінку (успіх або ре-рендер з помилками),
        # тому чекаємо на навігацію, інакше наступний крок може прочитати стару сторінку
        with self.page.expect_navigation():
            self.continue_button.click()

    def register(self, user):
        """Заповнює всю форму реєстрації даними user і надсилає її."""
        self.fill(user)
        self.submit()

    def error_for(self, field):
        """Повертає повідомлення .text-danger, прив'язане саме до цього поля."""
        return field.locator(
            "xpath=following-sibling::div[contains(@class, 'text-danger')]"
        )
