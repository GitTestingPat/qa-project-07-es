"""
Paquete de utilidades para tests automatizados con Selenium.

Este paquete contiene módulos helper para:
- Configuración de navegadores (browser_utils)
- Captura de tráfico de red (network_utils)
"""

from .browser_utils import (
    create_chrome_options,
    create_chrome_driver,
    enable_network_capture,
    get_chrome_version
)

from .network_utils import (
    extract_code_from_sms_request
)

__all__ = [
    # browser_utils
    'create_chrome_options',
    'create_chrome_driver',
    'enable_network_capture',
    'get_chrome_version',
    
    # network_utils
    'extract_code_from_sms_request',
]

__version__ = '1.0.0'