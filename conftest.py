"""
Configuración de fixtures para tests de Urban Routes.
"""
import pytest
from pages.urban_routes_page import UrbanRoutesPage
from utils.browser_utils import create_chrome_driver
import data


@pytest.fixture
def driver():
    """
    Crea y configura el driver de Chrome con todas las opciones necesarias.
    
    Yields:
        WebDriver: Instancia configurada de Chrome
    """
    driver = create_chrome_driver()
    yield driver
    driver.quit()


@pytest.fixture
def page(driver):
    """
    Inicializa la página UrbanRoutesPage.
    
    Args:
        driver: Fixture de WebDriver
        
    Returns:
        UrbanRoutesPage: Instancia del Page Object
    """
    return UrbanRoutesPage(driver)


@pytest.fixture
def page_with_url(page):
    """
    Abre la URL base antes de cada test.
    
    Args:
        page: Fixture de UrbanRoutesPage
        
    Returns:
        UrbanRoutesPage: Instancia con URL cargada
    """
    page.get_page(data.BASE_URL)
    return page