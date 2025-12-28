"""
Tests para validar que las utilidades funcionen correctamente.
"""
from selenium.webdriver.common.by import By


def test_browser_utils_creates_driver():
    """Verifica que se pueda crear un driver con browser_utils"""
    from utils.browser_utils import create_chrome_driver
    
    driver = create_chrome_driver()
    assert driver is not None
    assert driver.title is not None  # Driver funciona
    driver.quit()


def test_browser_utils_creates_options():
    """Verifica que se puedan crear opciones de Chrome"""
    from utils.browser_utils import create_chrome_options
    
    options = create_chrome_options()
    assert options is not None
    assert "--headless=new" in options.arguments


def test_wait_utils_with_real_page(page_with_url):
    """Verifica que wait_utils funcione con página real"""
    from utils.wait_utils import is_element_present
    
    # Buscar un elemento que sabemos que existe
    result = is_element_present(
        page_with_url.driver,
        (By.TAG_NAME, "body"),
        timeout=5
    )
    assert result is True


def test_validation_utils_url(page_with_url):
    """Verifica que validation_utils funcione"""
    from deprecated.validation_utils import validate_url
    import data
    
    # Validar que la URL actual sea correcta
    validate_url(page_with_url.driver, data.BASE_URL, exact_match=True)