from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class UrbanRoutesPage:
    FROM_FIELD = (By.XPATH, "//input[@id='from']")
    TO_FIELD = (By.XPATH, "//input[@id='to']")
    REQUEST_TAXI_BUTTON = (By.CLASS_NAME, "button.round")
    COMFORT_OPTION = (By.XPATH, "//div[contains(text(), 'Comfort')]")
    COMFORT_CATEGORY_BUTTON = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[normalize-space()='Comfort']]")
    PHONE_NUMBER_BUTTON = (By.XPATH, "//div[contains(text(), 'Phone number')]")
    PHONE_LABEL = (By.CSS_SELECTOR, "label[for='phone']")  # La etiqueta que está encima del botón de teléfono
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.CSS_SELECTOR, "form button.button.full")
    SMS_CODE_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[@class='button full' and @type='submit' and contains(text(), 'Confirm')]")
    RESEND_CODE_BUTTON = (By.XPATH, "//button[contains(text(), 'Vuelve a enviar el código')]")

    PAYMENT_ARROW = (By.XPATH, "//img[@alt='Arrow right']")
    ADD_CARD_BUTTON = (By.XPATH, "//div[text()='Agregar una tarjeta']")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    COMMENT_INPUT = (By.ID, "comment")
    BLANKETS_SLIDER = (By.CLASS_NAME, "slider")
    ICE_CREAM_PLUS_BUTTON = (By.CLASS_NAME, "counter-plus")
    ORDER_TAXI_BUTTON_FINAL = (By.CLASS_NAME, "smart-button-main")
    BENDER_IMAGE = (By.XPATH, "//img[@alt='close']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def get_page(self, url, timeout=20): 
        """Abre la página y espera que cargue completamente"""
        self.driver.get(url)
        try:
            # Esperar que aparezca el logo-disclaimer con el nombre PLATFORM
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "logo-disclaimer"))
            )
            print("✅ Página cargada correctamente")
        except Exception as e:
            print(f"⚠️ Error esperando 'logo-disclaimer': {e}")
            print(f"📄 Título después de espera: '{self.driver.title}'")

    def set_from_address(self, address):
        from_field = self.wait.until(EC.presence_of_element_located(self.FROM_FIELD))
        from_field.clear()
        from_field.send_keys(address)

    def set_to_address(self, address):
        to_field = self.wait.until(EC.presence_of_element_located(self.TO_FIELD))
        to_field.clear()
        to_field.send_keys(address)

    def click_request_taxi(self):
        button = self.wait.until(EC.element_to_be_clickable(self.REQUEST_TAXI_BUTTON))
        button.click()

    def select_comfort_category(self):
        # Esperar a que el panel de tarifas aparezca (espera al primer tcard)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tcard")))
        # Hacer clic en Comfort
        comfort = self.wait.until(EC.element_to_be_clickable(self.COMFORT_CATEGORY_BUTTON))
        comfort.click()
        
    def get_comfort_element(self):
        # Obtener el elemento de la categoría Comfort
        return self.wait.until(EC.visibility_of_element_located(self.COMFORT_CATEGORY_BUTTON))

    def click_phone_field(self):
        """Abre el modal de teléfono y activa el campo"""
        # Hacer clic en el div que abre el modal
        phone_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Phone number')]"))
        )
        phone_button.click()
        print("✅ Modal abierto y campo de teléfono listo")
        
        # Esperar que el input sea visible (el modal ya lo activa)
        self.wait.until(EC.visibility_of_element_located((By.ID, "phone")))
        
    def enter_phone_number(self, phone):
        """Ingresa el número de teléfono en el campo de entrada"""
        phone_input = self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(phone)

    def click_next_button(self):
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    # Método para ingresar el código de verificación
    def enter_sms_code(self, code):
        input_field = self.wait.until(EC.visibility_of_element_located(self.SMS_CODE_INPUT))
        input_field.clear()
        input_field.send_keys(code)
        
        # Dispara eventos manualmente si la app lo requiere
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_field)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input_field)
    
        print(f"✅ Código de SMS '{code}' ingresado.")

    # Método para hacer clic en Confirmar
    def click_confirm_button(self):
        from selenium.webdriver.support.ui import WebDriverWait
        
        # El botón ya está habilitado, solo necesitamos encontrarlo y hacer clic
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirm']"))
            )
            button.click()
            print("✅ Botón 'Confirm' clickeado.")
        except Exception as e:
            print(f"⚠️ Error al hacer clic en 'Confirm': {e}")
            # Intentar con JavaScript como respaldo
            button = self.driver.find_element(By.XPATH, "//button[text()='Confirm']")
            self.driver.execute_script("arguments[0].click();", button)
            print("✅ Botón 'Confirm' clickeado con JavaScript.")

    # Método para esperar que el modal esté visible
    def wait_for_sms_modal(self):
        self.wait.until(EC.visibility_of_element_located(self.SMS_CODE_INPUT))
        print("✅ Modal de SMS visible.")
        
    
    # Método para interceptar la respuesta de red y obtener el código SMS
    def get_sms_code_from_network(self, phone_number):
        """
        Intercepta la respuesta de red que contiene el código SMS.
        Busca una solicitud GET que contenga el número de teléfono y devuelva un JSON con "code".
        """
        print("🔍 Buscando código SMS en la red...")
        
        # Espera para asegurar que la solicitud se haya completado
        time.sleep(3)  # 

        logs = self.driver.get_log("performance")
        
        for log in logs:
            try:
                message = json.loads(log["message"])
                method = message.get("message", {}).get("method")
                params = message.get("message", {}).get("params", {})
                
                if method == "Network.responseReceived":
                    # Verifica que 'response' exista en params
                    if "response" not in params:
                        continue
                    
                    response = params["response"]
                    url = response.get("url", "")
                    
                    # Normaliza el número para coincidir con la URL (puede estar codificado)
                    normalized_phone = phone_number.replace("+", "%2B")  # Codificación URL del '+'
                    
                    if normalized_phone in url or phone_number in url:
                        request_id = params.get("requestId")
                        if not request_id:
                            continue
                        
                        try:
                            body = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                            data = json.loads(body["body"])
                            if "code" in data:
                                code = str(data["code"])
                                print(f"✅ Código SMS capturado: {code}")
                                return code
                        except Exception as e:
                            print(f"⚠️ No se pudo extraer el cuerpo de la respuesta: {e}")
                            continue
            except Exception:
                # Ignorar logs malformados o no relevantes
                continue
        raise Exception("❌ No se encontró el código SMS en las respuestas de red.")
    
    def debug_buttons_in_modal(self):
        """Método temporal para debugging - muestra todos los botones en el modal"""
        import time
        time.sleep(2)  # Esperar que el modal esté completamente cargado
        
        # Buscar todos los botones
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        
        print(f"\n🔍 Se encontraron {len(buttons)} botones en la página:")
        for i, button in enumerate(buttons):
            try:
                text = button.text
                classes = button.get_attribute("class")
                btn_type = button.get_attribute("type")
                is_displayed = button.is_displayed()
                is_enabled = button.is_enabled()
                
                print(f"\nBotón {i+1}:")
                print(f"  - Texto: '{text}'")
                print(f"  - Clases: '{classes}'")
                print(f"  - Type: '{btn_type}'")
                print(f"  - Visible: {is_displayed}")
                print(f"  - Habilitado: {is_enabled}")
            except Exception as e:
                print(f"  - Error al leer botón {i+1}: {e}")

    def click_payment_arrow(self):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_ARROW)).click()

    def click_add_card(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()

    def enter_card_number(self, number):
        card_num = self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_INPUT))
        card_num.clear()
        card_num.send_keys(number)

    def enter_card_code(self, code):
        card_code = self.wait.until(EC.presence_of_element_located(self.CARD_CODE_INPUT))
        card_code.clear()
        card_code.send_keys(code)

    def add_comment(self, comment):
        comment_input = self.wait.until(EC.presence_of_element_located(self.COMMENT_INPUT))
        comment_input.clear()
        comment_input.send_keys(comment)

    def activate_blankets(self):
        self.wait.until(EC.element_to_be_clickable(self.BLANKETS_SLIDER)).click()

    def add_ice_creams(self, quantity=2):
        plus_btn = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
        for _ in range(quantity):
            plus_btn.click()

    def click_order_taxi_final(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_TAXI_BUTTON_FINAL)).click()

    def wait_for_bender(self):
        return self.wait.until(EC.presence_of_element_located(self.BENDER_IMAGE))

    def is_from_address_set(self, expected_address):
        from_field = self.driver.find_element(*self.FROM_FIELD)
        return from_field.get_attribute("value") == expected_address

    def is_to_address_set(self, expected_address):
        to_field = self.driver.find_element(*self.TO_FIELD)
        return to_field.get_attribute("value") == expected_address