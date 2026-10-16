import pytest

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.data import generate_user_data


FIELD_LOCATORS = {
    "first_name": "firstname_input",
    "last_name": "lastname_input",
    "email": "email_input",
    "telephone": "telephone_input",
    "address": "address_input",
    "city": "city_input",
    "password": "password_input",
}

FIELD_ERRORS = {
    "first_name": "Ім`я повинно містити від 1 до 32 символів!",
    "last_name": "Прізвище повинно містити від 1 до 32 символів!",
    "email": "Неправильний E-Mail!",
    "telephone": "Телефон повинен містити від 3 до 32 символів!",
    "address": "Адреса 1 повинна містити від 3 до 128 символів!",
    "city": "Назва міста повинна містити від 2 до 128 символів!",
    "password": "Пароль повинен містити від 4 до 20 символів!",
}


def test_registration_creates_account(page):
    """Успішна реєстрація створює акаунт і одразу логінить користувача."""
    user = generate_user_data()

    register_page = RegisterPage(page)
    register_page.open()
    register_page.fill(user)

    assert register_page.country_select.input_value() != ""
    assert register_page.zone_select.input_value() != ""

    register_page.submit()

    assert register_page.success_heading.is_visible()
    assert "створено" in register_page.success_heading.inner_text()

    # Авто-логін: на сторінці доступне посилання виходу з акаунту
    assert "account/logout" in page.content()


@pytest.mark.parametrize(
    "field",
    ["first_name", "last_name", "email", "telephone", "address", "city", "password"],
)
def test_registration_required_field_validation(page, field):
    """Порожнє обов'язкове поле показує своє повідомлення, без хибних помилок на інших."""
    user = generate_user_data()
    user[field] = ""

    register_page = RegisterPage(page)
    register_page.open()
    register_page.register(user)

    assert "account/register" in page.url
    assert register_page.errors.count() > 0

    target_input = getattr(register_page, FIELD_LOCATORS[field])
    target_error = register_page.error_for(target_input)
    assert FIELD_ERRORS[field] in target_error.inner_text(), (
        f"Очікували повідомлення про поле '{field}'"
    )

    other_field = "last_name" if field != "last_name" else "first_name"
    other_input = getattr(register_page, FIELD_LOCATORS[other_field])
    other_error = register_page.error_for(other_input)
    assert other_error.count() == 0, (
        f"Поле '{other_field}' було заповнене коректно, але показує помилку"
    )


def test_duplicate_email_keeps_original_account_intact(page):
    """Повторна реєстрація з тим email відхиляється, оригінальний акаунт лишається робочим."""
    user = generate_user_data()

    register_page = RegisterPage(page)
    register_page.open()
    register_page.register(user)
    assert "account/success" in page.url, "Перша реєстрація мала завершитись успіхом"

    login_page = LoginPage(page)
    login_page.logout()

    register_page.open()
    register_page.register(user)

    assert "account/register" in page.url, "Повторна реєстрація не мала пройти"
    assert register_page.duplicate_email_alert.is_visible()
    assert "вже зареєстровано" in register_page.duplicate_email_alert.inner_text()

    login_page.open()
    login_page.login(user["email"], user["password"])

    assert "account/account" in page.url, "Логін з оригінальними даними мав спрацювати"
    assert login_page.wrong_credentials_alert.count() == 0
