"""
Paquete de utilidades para tests automatizados con Selenium.

Este paquete contiene módulos helper para:
- Configuración de navegadores (browser_utils)
- Esperas y sincronización (wait_utils)
- Validaciones comunes (validation_utils)
- Captura de tráfico de red (network_utils)
"""

from .browser_utils import (
    create_chrome_options,
    create_chrome_driver,
    enable_network_capture,
    get_chrome_version
)

from .wait_utils import (
    wait_for_element,
    wait_for_element_to_be_clickable,
    wait_for_element_visible,
    wait_for_text_in_element,
    is_element_visible,
    is_element_present
)

from .validation_utils import (
    validate_text_in_element,
    validate_element_visible_and_enabled,
    validate_field_value,
    validate_text_in_page_source,
    validate_url,
    validate_title
)

from .network_utils import (
    get_network_logs,
    extract_code_from_sms_request,
    wait_for_network_idle,
    find_request_by_url_pattern
)

__all__ = [
    # browser_utils
    'create_chrome_options',
    'create_chrome_driver',
    'enable_network_capture',
    'get_chrome_version',
    
    # wait_utils
    'wait_for_element',
    'wait_for_element_to_be_clickable',
    'wait_for_element_visible',
    'wait_for_text_in_element',
    'is_element_visible',
    'is_element_present',
    
    # validation_utils
    'validate_text_in_element',
    'validate_element_visible_and_enabled',
    'validate_field_value',
    'validate_text_in_page_source',
    'validate_url',
    'validate_title',
    
    # network_utils
    'get_network_logs',
    'extract_code_from_sms_request',
    'wait_for_network_idle',
    'find_request_by_url_pattern',
]

__version__ = '1.0.0'
