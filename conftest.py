import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.urban_routes_page import UrbanRoutesPage
import data

# Fixture para inicializar y cerrar el driver de Selenium
@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-notifications")
    # options.add_argument("--disable-infobars")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--start-maximized")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    # Habilitar el registro de red para CDP
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Habilitar la red en CDP
    driver.execute_cdp_cmd("Network.enable", {})
    
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Fixture para inicializar la página UrbanRoutesPage    
@pytest.fixture
def page(driver):
    return UrbanRoutesPage(driver)

# Fixture para abrir la URL base antes de cada test que lo requiera
@pytest.fixture
def page_with_url(page):
    page.get_page(data.BASE_URL)
    return page

# Fixture para abrir la URL base y habilitar CDP (Chrome DevTools Protocol) antes de cada test que lo requiera
# Para capturar tráfico de red o realizar otras acciones avanzadas
@pytest.fixture
def page_with_url_and_cdp(driver, data):
    driver.get(data.BASE_URL)
    page = UrbanRoutesPage(driver)
    return page