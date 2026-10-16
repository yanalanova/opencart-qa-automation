import time


def unique_email(prefix: str = "user") -> str:
    """Генерує унікальний email, щоб кожен запуск тесту реєстрував нового користувача."""
    return f"{prefix}_{int(time.time() * 1000)}@example.com"


def generate_user_data() -> dict:
    """Повертає повний набір синтетичних (несправжніх) даних для реєстрації."""
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": unique_email(),
        "telephone": "0501234567",
        "address": "1 Test Street",
        "city": "Kyiv",
        "country": "Ukraine",
        "zone": "Kyiv",
        "password": "Test1234!",
    }
