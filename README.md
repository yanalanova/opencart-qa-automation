# opencart-qa-automation

UI-автотести для демо-магазину [demo.opencart.ua](https://demo.opencart.ua), написані на Python з Playwright і pytest за патерном Page Object.

## Структура

| Шлях | Призначення |
| --- | --- |
| `config.py` | `BASE_URL` — єдине джерело правди для адреси сайту |
| `pages/base_page.py` | `BasePage` — батьківський клас усіх Page Object'ів, уміє відкривати шлях відносно `BASE_URL` |
| `pages/home_page.py` | `HomePage` — картки Featured, додавання в кошик, лічильник кошика |
| `pages/product_page.py` | `ProductPage` — заголовок товару і кнопка `#button-cart` |
| `pages/cart_page.py` | `CartPage` — позиції кошика |
| `conftest.py` | pytest-фікстури |
| `pytest.ini` | опції запуску pytest-playwright |
| `tests/` | тести |

Усі перевірки живуть у тестах через звичайний `assert`. Page Object'и містять тільки локатори та дії — без жодного `assert` і без `expect()`.

## Запуск

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
playwright install
pytest
```

## Робочий процес

Кожен урок виконується в окремій гілці (`lesson-00`, `lesson-01`, …) і потрапляє в `main` лише через Pull Request з рев'ю. Прямі коміти в `main` не робляться.
