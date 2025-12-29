"""
Utilidades para esperas y sincronización en tests con Selenium.

Este módulo proporciona funciones helper para manejar esperas explícitas
y evitar código repetitivo en Page Objects y tests.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def wait_for_element(driver, locator, timeout=10):
    """
    Espera que un elemento esté presente en el DOM.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        WebElement: Elemento encontrado
        None: Si se alcanza el timeout
        
    Example:
        >>> from selenium.webdriver.common.by import By
        >>> element = wait_for_element(driver, (By.ID, "username"))
    """
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    except TimeoutException:
        print(f"⏱️ Timeout: Elemento {locator} no encontrado en {timeout}s")
        return None


def wait_for_element_to_be_clickable(driver, locator, timeout=10):
    """
    Espera que un elemento sea clickeable (visible y habilitado).
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        WebElement: Elemento clickeable
        None: Si se alcanza el timeout
        
    Example:
        >>> button = wait_for_element_to_be_clickable(driver, (By.ID, "submit"))
        >>> if button:
        ...     button.click()
    """
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    except TimeoutException:
        print(f"⏱️ Timeout: Elemento {locator} no clickeable en {timeout}s")
        return None


def wait_for_element_visible(driver, locator, timeout=10):
    """
    Espera que un elemento sea visible en la página.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        WebElement: Elemento visible
        None: Si se alcanza el timeout
        
    Example:
        >>> modal = wait_for_element_visible(driver, (By.CLASS_NAME, "modal"))
    """
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    except TimeoutException:
        print(f"⏱️ Timeout: Elemento {locator} no visible en {timeout}s")
        return None


def wait_for_text_in_element(driver, locator, text, timeout=10):
    """
    Espera que un texto específico aparezca en un elemento.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        text (str): Texto esperado
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si el texto aparece, False si timeout
        
    Example:
        >>> success = wait_for_text_in_element(
        ...     driver,
        ...     (By.ID, "status"),
        ...     "Completado"
        ... )
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.text_to_be_present_in_element(locator, text))
        return True
    except TimeoutException:
        print(f"⏱️ Timeout: Texto '{text}' no encontrado en {locator} en {timeout}s")
        return False


def wait_for_text_in_element_value(driver, locator, text, timeout=10):
    """
    Espera que un texto específico aparezca en el valor de un input.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        text (str): Texto esperado en el value
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si el texto aparece, False si timeout
        
    Example:
        >>> wait_for_text_in_element_value(
        ...     driver,
        ...     (By.ID, "address"),
        ...     "123 Main St"
        ... )
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.text_to_be_present_in_element_value(locator, text))
        return True
    except TimeoutException:
        print(f"⏱️ Timeout: Valor '{text}' no encontrado en {locator} en {timeout}s")
        return False


def wait_for_element_to_disappear(driver, locator, timeout=10):
    """
    Espera que un elemento desaparezca del DOM.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si el elemento desaparece, False si timeout
        
    Example:
        >>> wait_for_element_to_disappear(driver, (By.CLASS_NAME, "loading"))
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until_not(EC.presence_of_element_located(locator))
        return True
    except TimeoutException:
        print(f"⏱️ Timeout: Elemento {locator} sigue presente después de {timeout}s")
        return False


def is_element_visible(driver, locator, timeout=5):
    """
    Verifica si un elemento está visible (wrapper de conveniencia).
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si visible, False si no
        
    Example:
        >>> if is_element_visible(driver, (By.ID, "error-message")):
        ...     print("Hay un error visible")
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element.is_displayed()
    except (TimeoutException, NoSuchElementException):
        return False


def is_element_present(driver, locator, timeout=5):
    """
    Verifica si un elemento está presente en el DOM (no necesariamente visible).
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si presente, False si no
        
    Example:
        >>> if is_element_present(driver, (By.ID, "hidden-field")):
        ...     print("El elemento existe en el DOM")
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located(locator))
        return True
    except TimeoutException:
        return False


def wait_for_number_of_elements(driver, locator, count, timeout=10):
    """
    Espera que haya exactamente N elementos que coincidan con el localizador.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        count (int): Número exacto de elementos esperados
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        list: Lista de elementos encontrados
        None: Si se alcanza el timeout
        
    Example:
        >>> items = wait_for_number_of_elements(
        ...     driver,
        ...     (By.CLASS_NAME, "product"),
        ...     5
        ... )
    """
    try:
        wait = WebDriverWait(driver, timeout)
        
        def check_count(driver):
            elements = driver.find_elements(*locator)
            return elements if len(elements) == count else False
        
        return wait.until(check_count)
    except TimeoutException:
        print(f"⏱️ Timeout: No se encontraron {count} elementos {locator} en {timeout}s")
        return None


def wait_for_url_contains(driver, text, timeout=10):
    """
    Espera que la URL contenga un texto específico.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        text (str): Texto esperado en la URL
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si la URL contiene el texto, False si timeout
        
    Example:
        >>> wait_for_url_contains(driver, "dashboard")
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.url_contains(text))
        return True
    except TimeoutException:
        print(f"⏱️ Timeout: URL no contiene '{text}' después de {timeout}s")
        return False


def wait_for_alert(driver, timeout=10):
    """
    Espera que aparezca una alerta de JavaScript.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        Alert: Objeto Alert si aparece
        None: Si se alcanza el timeout
        
    Example:
        >>> alert = wait_for_alert(driver)
        >>> if alert:
        ...     alert.accept()
    """
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.alert_is_present())
    except TimeoutException:
        print(f"⏱️ Timeout: Alerta no apareció en {timeout}s")
        return None
