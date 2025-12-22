"""
Utilidades para configuración del navegador Chrome.

Este módulo contiene funciones para crear y configurar instancias
de Chrome WebDriver optimizadas para testing automatizado.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_options():
    """
    Crea y configura las opciones de Chrome optimizadas para testing.
    
    Incluye configuraciones para:
    - Modo headless
    - Desactivación de características innecesarias
    - Optimización de rendimiento
    - Habilitación de CDP para captura de red
    
    Returns:
        Options: Objeto con todas las opciones configuradas
        
    Example:
        >>> options = create_chrome_options()
        >>> driver = webdriver.Chrome(options=options)
    """
    options = Options()
    
    # Configuración básica
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Desactivar características innecesarias
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    
    # Optimizaciones de rendimiento
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    
    # Habilitar el registro de red para CDP (Chrome DevTools Protocol)
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    return options


def create_chrome_driver(options=None, implicit_wait=10):
    """
    Crea una instancia de Chrome WebDriver con configuración completa.
    
    Args:
        options (Options, optional): Opciones personalizadas de Chrome.
            Si no se proporciona, usa create_chrome_options().
        implicit_wait (int, optional): Tiempo de espera implícita en segundos.
            Por defecto 10 segundos.
        
    Returns:
        WebDriver: Instancia configurada de Chrome con CDP habilitado
        
    Example:
        >>> driver = create_chrome_driver()
        >>> driver.get("https://example.com")
        >>> driver.quit()
        
    Example con opciones personalizadas:
        >>> custom_options = create_chrome_options()
        >>> custom_options.add_argument("--start-maximized")
        >>> driver = create_chrome_driver(options=custom_options)
    """
    # Usar opciones por defecto si no se proporcionan
    if options is None:
        options = create_chrome_options()
    
    # Configurar el servicio de ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # Crear instancia del driver
    driver = webdriver.Chrome(service=service, options=options)
    
    # Habilitar la red en CDP para captura de tráfico
    driver.execute_cdp_cmd("Network.enable", {})
    
    # Configurar tiempo de espera implícita
    driver.implicitly_wait(implicit_wait)
    
    return driver


def enable_network_capture(driver):
    """
    Habilita la captura de tráfico de red en un driver existente.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        
    Example:
        >>> driver = webdriver.Chrome()
        >>> enable_network_capture(driver)
    """
    driver.execute_cdp_cmd("Network.enable", {})


def get_chrome_version(driver):
    """
    Obtiene la versión de Chrome del driver.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        
    Returns:
        dict: Información de versión del navegador
        
    Example:
        >>> driver = create_chrome_driver()
        >>> version_info = get_chrome_version(driver)
        >>> print(version_info)
    """
    return driver.capabilities.get('browserVersion', 'unknown')
