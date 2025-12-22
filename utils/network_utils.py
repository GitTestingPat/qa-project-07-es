"""
Utilidades para captura de tráfico de red con Chrome DevTools Protocol (CDP).

Este módulo proporciona funciones para interceptar y analizar
el tráfico de red del navegador, útil para capturar códigos SMS,
validar requests/responses, y debugging.
"""

import time
import json
from typing import Optional, List, Dict, Any


def get_network_logs(driver) -> List[Dict[str, Any]]:
    """
    Obtiene todos los logs de red del navegador.
    
    Args:
        driver (WebDriver): Instancia de WebDriver con CDP habilitado
        
    Returns:
        list: Lista de logs de performance del navegador
        
    Example:
        >>> logs = get_network_logs(driver)
        >>> print(f"Se capturaron {len(logs)} eventos de red")
    """
    return driver.get_log("performance")


def extract_code_from_sms_request(phone_number: str, driver, timeout: int = 60) -> str:
    """
    Extrae el código SMS del tráfico de red capturado por CDP.
    
    Esta función monitorea el tráfico de red en busca de requests
    relacionados con el número de teléfono y extrae el código SMS
    de la respuesta.
    
    Args:
        phone_number (str): Número de teléfono usado en el request
        driver (WebDriver): Instancia de WebDriver con CDP habilitado
        timeout (int): Tiempo máximo de espera en segundos (default: 60)
        
    Returns:
        str: Código SMS extraído
        
    Raises:
        Exception: Si no se encuentra el código en el tiempo dado
        
    Example:
        >>> code = extract_code_from_sms_request("+1234567890", driver)
        >>> print(f"Código SMS recibido: {code}")
        
    Note:
        El driver debe tener CDP habilitado con:
        driver.execute_cdp_cmd("Network.enable", {})
    """
    start_time = time.time()
    last_log_count = 0
    
    print(f"🔍 Buscando código SMS para número: {phone_number}")
    print(f"⏱️  Timeout configurado: {timeout}s")
    
    while time.time() - start_time < timeout:
        logs = get_network_logs(driver)
        
        # Solo procesar logs nuevos
        new_logs = logs[last_log_count:]
        last_log_count = len(logs)
        
        for log in new_logs:
            try:
                message = json.loads(log["message"])
                method = message.get("message", {}).get("method", "")
                
                # Buscar respuestas de red
                if method == "Network.responseReceived":
                    params = message["message"]["params"]
                    response_url = params["response"]["url"]
                    
                    # Verificar si la URL contiene el número de teléfono
                    if f"number={phone_number}" in response_url:
                        print(f"✅ URL encontrada: {response_url}")
                        request_id = params["requestId"]
                        
                        # Intentar obtener el body de la respuesta
                        code = _extract_code_from_response_body(driver, request_id, logs)
                        if code:
                            print(f"🎉 Código SMS capturado: {code}")
                            return code
                            
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # Log mal formado o sin datos relevantes
                continue
        
        # Esperar un poco antes de revisar de nuevo
        time.sleep(1)
        
        # Mostrar progreso cada 10 segundos
        elapsed = int(time.time() - start_time)
        if elapsed % 10 == 0 and elapsed > 0:
            print(f"⏱️  Esperando... {elapsed}s / {timeout}s")
    
    # Si llegamos aquí, se agotó el timeout
    raise Exception(
        f"❌ No se pudo obtener el código SMS en {timeout}s. "
        f"Verifica que:\n"
        f"  1. El número de teléfono '{phone_number}' sea correcto\n"
        f"  2. El request SMS se haya enviado correctamente\n"
        f"  3. CDP esté habilitado en el driver"
    )


def _extract_code_from_response_body(driver, request_id: str, logs: List) -> Optional[str]:
    """
    Extrae el código del body de una respuesta HTTP.
    
    Función auxiliar interna para extract_code_from_sms_request.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        request_id (str): ID del request cuyo body queremos extraer
        logs (list): Lista de logs de red
        
    Returns:
        str: Código extraído o None si no se encuentra
    """
    try:
        # Buscar el evento de carga completada
        for log in logs:
            try:
                inner_message = json.loads(log["message"])
                inner_method = inner_message.get("message", {}).get("method", "")
                
                if (inner_method == "Network.loadingFinished" and 
                    inner_message["message"]["params"]["requestId"] == request_id):
                    
                    # Obtener el body de la respuesta usando CDP
                    response_body = driver.execute_cdp_cmd(
                        "Network.getResponseBody",
                        {"requestId": request_id}
                    )
                    
                    body = response_body.get("body", "")
                    if not body:
                        return None
                    
                    # Parsear JSON y extraer código
                    data = json.loads(body)
                    code = data.get("code")
                    
                    if code:
                        return code
                        
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
                
    except Exception as e:
        print(f"⚠️  Error al extraer código del body: {e}")
    
    return None


def wait_for_network_idle(driver, timeout: int = 5):
    """
    Espera que no haya actividad de red.
    
    Útil para asegurar que todas las requests se hayan completado
    antes de continuar con el test.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        timeout (int): Tiempo a esperar sin actividad en segundos
        
    Example:
        >>> driver.get("https://example.com")
        >>> wait_for_network_idle(driver, timeout=3)
        >>> # Ahora sabemos que la página cargó completamente
    """
    print(f"⏸️  Esperando {timeout}s para estabilizar red...")
    time.sleep(timeout)


def find_request_by_url_pattern(driver, url_pattern: str, timeout: int = 30) -> Optional[Dict]:
    """
    Busca un request que coincida con un patrón de URL.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        url_pattern (str): Patrón a buscar en las URLs (substring)
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        dict: Información del request encontrado o None
        
    Example:
        >>> request = find_request_by_url_pattern(driver, "api/users")
        >>> if request:
        ...     print(f"Request ID: {request['requestId']}")
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        logs = get_network_logs(driver)
        
        for log in logs:
            try:
                message = json.loads(log["message"])
                method = message.get("message", {}).get("method", "")
                
                if method == "Network.requestWillBeSent":
                    params = message["message"]["params"]
                    request_url = params["request"]["url"]
                    
                    if url_pattern in request_url:
                        return {
                            "requestId": params["requestId"],
                            "url": request_url,
                            "method": params["request"]["method"],
                            "timestamp": params["timestamp"]
                        }
                        
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        
        time.sleep(0.5)
    
    return None


def get_all_requests_to_domain(driver, domain: str) -> List[Dict]:
    """
    Obtiene todos los requests realizados a un dominio específico.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        domain (str): Dominio a buscar (ej: "api.example.com")
        
    Returns:
        list: Lista de diccionarios con información de requests
        
    Example:
        >>> requests = get_all_requests_to_domain(driver, "api.urbanroutes.com")
        >>> print(f"Se realizaron {len(requests)} requests a la API")
    """
    logs = get_network_logs(driver)
    requests = []
    
    for log in logs:
        try:
            message = json.loads(log["message"])
            method = message.get("message", {}).get("method", "")
            
            if method == "Network.requestWillBeSent":
                params = message["message"]["params"]
                request_url = params["request"]["url"]
                
                if domain in request_url:
                    requests.append({
                        "url": request_url,
                        "method": params["request"]["method"],
                        "timestamp": params["timestamp"]
                    })
                    
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    
    return requests


def clear_network_logs(driver):
    """
    Limpia los logs de red acumulados.
    
    Nota: Esta función solo lee los logs para "consumirlos",
    ya que Selenium no tiene una forma directa de limpiarlos.
    
    Args:
        driver (WebDriver): Instancia de WebDriver
        
    Example:
        >>> clear_network_logs(driver)
        >>> # Ahora solo se capturarán logs nuevos
    """
    _ = get_network_logs(driver)
    print("🧹 Logs de red consumidos")
