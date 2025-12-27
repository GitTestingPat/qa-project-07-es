"""
Utilidades para captura de tráfico de red con Chrome DevTools Protocol (CDP).

Este módulo proporciona funciones para interceptar y analizar
el tráfico de red del navegador, útil para capturar códigos SMS.
"""

import time
import json


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
    
    print(f"🔍 Buscando código SMS en tráfico de red para: {phone_number}")
    print(f"⏱️  Timeout: {timeout}s")
    
    while time.time() - start_time < timeout:
        logs = driver.get_log("performance")
        
        for log in logs:
            try:
                message = json.loads(log["message"])
                method = message.get("message", {}).get("method", "")
                
                if method == "Network.responseReceived":
                    params = message["message"]["params"]
                    response_url = params["response"]["url"]
                    
                    # Verificar si la URL contiene el número de teléfono
                    if f"number={phone_number}" in response_url:
                        print(f"✅ URL encontrada que contiene el número: {response_url}")
                        request_id = params["requestId"]
                        
                        # Buscar el loading finished correspondiente
                        for inner_log in logs:
                            try:
                                inner_message = json.loads(inner_log["message"])
                                inner_method = inner_message.get("message", {}).get("method", "")
                                
                                if (inner_method == "Network.loadingFinished" and 
                                    inner_message["message"]["params"]["requestId"] == request_id):
                                    
                                    # Obtener el body de la respuesta
                                    try:
                                        response_body = driver.execute_cdp_cmd(
                                            "Network.getResponseBody",
                                            {"requestId": request_id}
                                        )
                                        
                                        body = response_body.get("body", "")
                                        if body:
                                            # Parsear JSON y extraer código
                                            data = json.loads(body)
                                            code = data.get("code")
                                            
                                            if code:
                                                print(f"🎉 Código SMS capturado exitosamente: {code}")
                                                return str(code)
                                    except Exception as e:
                                        print(f"⚠️ Error al obtener el body de la respuesta: {e}")
                                        # Continuar buscando si hay error al obtener el body
                                        continue
                                        
                            except (json.JSONDecodeError, KeyError, TypeError):
                                continue
                                
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        
        # Esperar un poco antes de revisar de nuevo
        time.sleep(1)
        
        # Mostrar progreso cada 10 segundos
        elapsed = int(time.time() - start_time)
        if elapsed % 10 == 0 and elapsed > 0:
            print(f"⏱️  Esperando código SMS... {elapsed}s transcurridos")
    
    # Si llegamos aquí, se agotó el timeout
    raise Exception(
        f"❌ No se pudo obtener el código SMS en {timeout}s.\n"
        f"Posibles causas:\n"
        f"  1. El número de teléfono '{phone_number}' no es válido\n"
        f"  2. El request SMS no se envió correctamente\n"
        f"  3. CDP no está habilitado en el driver\n"
        f"  4. La respuesta del servidor tardó más de {timeout}s"
    )