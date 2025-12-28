"""
Utilidades para validaciones comunes en tests automatizados.

Este módulo proporciona funciones para validar elementos web
y reducir código repetitivo en tests.
"""


def validate_text_in_element(element, expected_text, field_name="elemento"):
    """
    Valida que un elemento contenga el texto esperado.
    
    Args:
        element (WebElement): Elemento a validar
        expected_text (str): Texto esperado
        field_name (str): Nombre descriptivo del campo para mensajes de error
        
    Raises:
        AssertionError: Si alguna validación falla
        
    Example:
        >>> element = driver.find_element(By.ID, "title")
        >>> validate_text_in_element(element, "Welcome", "título")
    """
    assert element is not None, f"❌ {field_name} es None"
    
    actual_text = element.text
    assert actual_text != "", f"❌ El texto de {field_name} está vacío"
    assert actual_text.strip() != "", f"❌ El texto de {field_name} contiene solo espacios"
    assert expected_text in actual_text, (
        f"❌ '{expected_text}' no encontrado en {field_name}: '{actual_text}'"
    )


def validate_element_visible_and_enabled(element, field_name="elemento"):
    """
    Valida que un elemento esté visible y habilitado.
    
    Args:
        element (WebElement): Elemento a validar
        field_name (str): Nombre descriptivo del campo para mensajes de error
        
    Raises:
        AssertionError: Si alguna validación falla
        
    Returns:
        WebElement: El mismo elemento (permite encadenar validaciones)
        
    Example:
        >>> button = driver.find_element(By.ID, "submit")
        >>> validate_element_visible_and_enabled(button, "botón de envío")
        >>> button.click()  # Sabemos que está listo para click
    """
    assert element is not None, f"❌ {field_name} es None"
    assert element.is_displayed(), f"❌ {field_name} no está visible"
    assert element.is_enabled(), f"❌ {field_name} no está habilitado"
    
    return element


def validate_element_visible(element, field_name="elemento"):
    """
    Valida que un elemento esté visible.
    
    Args:
        element (WebElement): Elemento a validar
        field_name (str): Nombre descriptivo del campo para mensajes de error
        
    Raises:
        AssertionError: Si alguna validación falla
        
    Returns:
        WebElement: El mismo elemento
        
    Example:
        >>> image = driver.find_element(By.TAG_NAME, "img")
        >>> validate_element_visible(image, "imagen del producto")
    """
    assert element is not None, f"❌ {field_name} es None"
    assert element.is_displayed(), f"❌ {field_name} no está visible"
    
    return element


def validate_field_value(driver, locator, expected_value, field_name="campo"):
    """
    Valida el valor de un input usando JavaScript para obtener el valor real.
    
    Útil para campos de input donde element.text no funciona correctamente.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        expected_value (str): Valor esperado
        field_name (str): Nombre descriptivo del campo para mensajes de error
        
    Raises:
        AssertionError: Si alguna validación falla
        
    Example:
        >>> from selenium.webdriver.common.by import By
        >>> validate_field_value(
        ...     driver,
        ...     (By.ID, "address"),
        ...     "123 Main St",
        ...     "dirección"
        ... )
    """
    element = driver.find_element(*locator)
    actual_value = driver.execute_script("return arguments[0].value;", element)
    
    assert actual_value != "", f"❌ El {field_name} está vacío"
    assert actual_value.strip() != "", f"❌ El {field_name} contiene solo espacios"
    assert actual_value == expected_value, (
        f"❌ {field_name} no coincide. "
        f"Esperado: '{expected_value}', "
        f"Obtenido: '{actual_value}'"
    )


def validate_text_in_page_source(driver, expected_text, case_sensitive=True):
    """
    Valida que un texto esté presente en el código fuente de la página.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        expected_text (str): Texto esperado
        case_sensitive (bool): Si la búsqueda es sensible a mayúsculas
        
    Raises:
        AssertionError: Si alguna validación falla
        
    Returns:
        bool: True si el texto se encuentra
        
    Example:
        >>> validate_text_in_page_source(driver, "Welcome to our site")
        >>> # Para búsqueda insensible a mayúsculas:
        >>> validate_text_in_page_source(driver, "welcome", case_sensitive=False)
    """
    page_source = driver.page_source
    
    assert page_source is not None, "❌ El código fuente de la página es None"
    assert len(page_source) > 0, "❌ El código fuente de la página está vacío"
    
    if case_sensitive:
        condition = expected_text in page_source
    else:
        condition = expected_text.lower() in page_source.lower()
    
    assert condition, f"❌ '{expected_text}' no encontrado en el código fuente"
    
    return True


def validate_url(driver, expected_url, exact_match=True):
    """
    Valida que la URL actual coincida con la esperada.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        expected_url (str): URL esperada
        exact_match (bool): Si debe ser coincidencia exacta o solo contener
        
    Raises:
        AssertionError: Si la URL no coincide
        
    Example:
        >>> validate_url(driver, "https://example.com/dashboard")
        >>> # Para validar que contenga parte de la URL:
        >>> validate_url(driver, "/dashboard", exact_match=False)
    """
    current_url = driver.current_url
    
    if exact_match:
        assert current_url == expected_url, (
            f"❌ URL no coincide. "
            f"Esperado: {expected_url}, "
            f"Actual: {current_url}"
        )
    else:
        assert expected_url in current_url, (
            f"❌ '{expected_url}' no encontrado en URL actual: {current_url}"
        )


def validate_title(driver, expected_title, partial_match=False):
    """
    Valida el título de la página.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        expected_title (str): Título esperado
        partial_match (bool): Si True, valida que contenga el texto
        
    Raises:
        AssertionError: Si el título no coincide
        
    Example:
        >>> validate_title(driver, "Home - Example Site")
        >>> # Para validación parcial:
        >>> validate_title(driver, "Example", partial_match=True)
    """
    actual_title = driver.title
    
    assert actual_title != "", "❌ El título de la página está vacío"
    assert len(actual_title) > 0, "❌ El título no tiene contenido"
    
    if partial_match:
        assert expected_title in actual_title, (
            f"❌ '{expected_title}' no encontrado en título: '{actual_title}'"
        )
    else:
        assert actual_title == expected_title, (
            f"❌ Título no coincide. "
            f"Esperado: '{expected_title}', "
            f"Actual: '{actual_title}'"
        )


def validate_element_attribute(element, attribute, expected_value, field_name="elemento"):
    """
    Valida que un atributo de un elemento tenga el valor esperado.
    
    Args:
        element (WebElement): Elemento a validar
        attribute (str): Nombre del atributo (ej: "class", "id", "value")
        expected_value (str): Valor esperado del atributo
        field_name (str): Nombre descriptivo del campo
        
    Raises:
        AssertionError: Si el atributo no coincide
        
    Example:
        >>> button = driver.find_element(By.ID, "submit")
        >>> validate_element_attribute(button, "class", "btn-primary", "botón")
    """
    actual_value = element.get_attribute(attribute)
    
    assert actual_value is not None, (
        f"❌ Atributo '{attribute}' no existe en {field_name}"
    )
    assert expected_value in actual_value, (
        f"❌ Atributo '{attribute}' de {field_name} no contiene '{expected_value}'. "
        f"Valor actual: '{actual_value}'"
    )


def validate_element_has_class(element, class_name, field_name="elemento"):
    """
    Valida que un elemento tenga una clase CSS específica.
    
    Args:
        element (WebElement): Elemento a validar
        class_name (str): Nombre de la clase CSS
        field_name (str): Nombre descriptivo del campo
        
    Raises:
        AssertionError: Si la clase no está presente
        
    Example:
        >>> card = driver.find_element(By.ID, "card-1")
        >>> validate_element_has_class(card, "active", "tarjeta")
    """
    class_attribute = element.get_attribute("class")
    
    assert class_attribute is not None, (
        f"❌ No se pudo obtener el atributo 'class' de {field_name}"
    )
    assert class_name in class_attribute, (
        f"❌ Clase '{class_name}' no encontrada en {field_name}. "
        f"Clases actuales: '{class_attribute}'"
    )


def validate_elements_count(driver, locator, expected_count, description="elementos"):
    """
    Valida que haya exactamente N elementos que coincidan con el localizador.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        locator (tuple): Tupla (By.TYPE, "value")
        expected_count (int): Número esperado de elementos
        description (str): Descripción de los elementos
        
    Raises:
        AssertionError: Si el conteo no coincide
        
    Example:
        >>> from selenium.webdriver.common.by import By
        >>> validate_elements_count(
        ...     driver,
        ...     (By.CLASS_NAME, "product"),
        ...     5,
        ...     "productos"
        ... )
    """
    elements = driver.find_elements(*locator)
    actual_count = len(elements)
    
    assert actual_count == expected_count, (
        f"❌ Número de {description} no coincide. "
        f"Esperado: {expected_count}, "
        f"Encontrado: {actual_count}"
    )
