# opencart-qa-automation

UI-автотести для демо-магазину [demo.opencart.ua](https://demo.opencart.ua), написані на Python з Playwright і pytest за патерном Page Object.

## Структура

| Шлях | Призначення |
| --- | --- |
| `config.py` | `BASE_URL` — єдине джерело правди для адреси сайту |
| `pages/base_page.py` | `BasePage` — батьківський клас усіх Page Object'ів, уміє відкривати шлях відносно `BASE_URL` |
| `pages/home_page.py` | `HomePage` — Page Object головної сторінки |
| `conftest.py` | pytest-фікстури |
| `pytest.ini` | опції запуску pytest-playwright |
| `tests/` | тести |

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
