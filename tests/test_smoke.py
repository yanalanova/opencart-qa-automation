from pages.home_page import HomePage


def test_home_page_loads(page):
    home = HomePage(page)
    home.open()
    assert "OpenCart" in page.title()
