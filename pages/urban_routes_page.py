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

    # Localizador para el botón Método de pago
    PAYMENT_METHOD_BUTTON = (By.XPATH, "//div[@class='pp-button filled']")  

    # Localizador para Agregar tarjeta
    ADD_CARD_BUTTON = (By.XPATH, "//div[@class='pp-title' and text()='Add a card']")
    
    # Localizadores para el campo Número de tarjeta
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

    # def debug_add_card_elements(self):
    #     """Método temporal para debugging - muestra elementos con 'tarjeta' o 'card'"""
    #     import time
    #     time.sleep(2)
        
    #     # Buscar por clase pp-title
    #     titles = self.driver.find_elements(By.CLASS_NAME, "pp-title")
    #     print(f"\n🔍 Elementos con clase 'pp-title': {len(titles)}")
    #     for i, title in enumerate(titles):
    #         try:
    #             text = title.text
    #             classes = title.get_attribute("class")
    #             is_displayed = title.is_displayed()
    #             print(f"\nElemento {i+1}:")
    #             print(f"  - Texto: '{text}'")
    #             print(f"  - Clases: '{classes}'")
    #             print(f"  - Visible: {is_displayed}")
    #         except Exception as e:
    #             print(f"  - Error: {e}")
        
    #     # Buscar todos los divs visibles
    #     divs = self.driver.find_elements(By.TAG_NAME, "div")
    #     print(f"\n🔍 Buscando divs con 'tarjeta' o 'card' en el texto...")
    #     for div in divs:
    #         try:
    #             text = div.text
    #             if 'tarjeta' in text.lower() or 'card' in text.lower():
    #                 classes = div.get_attribute("class")
    #                 is_displayed = div.is_displayed()
    #                 if is_displayed:
    #                     print(f"\n  - Texto: '{text}'")
    #                     print(f"  - Clases: '{classes}'")
    #         except Exception:
    #             pass
    
    # Método para abrir la página y espera que cargue completamente     
    def get_page(self, url, timeout=20): 
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


    # Método para establecer la dirección de origen
    def set_from_address(self, address):
        from_field = self.wait.until(EC.presence_of_element_located(self.FROM_FIELD))
        from_field.clear()
        from_field.send_keys(address)


    # Método para establecer la dirección de destino
    def set_to_address(self, address):
        to_field = self.wait.until(EC.presence_of_element_located(self.TO_FIELD))
        to_field.clear()
        to_field.send_keys(address)


    # Método para hacer clic en el botón Pedir un taxi
    def click_request_taxi(self):
        button = self.wait.until(EC.element_to_be_clickable(self.REQUEST_TAXI_BUTTON))
        button.click()


    # Método para seleccionar la categoría Comfort
    def select_comfort_category(self):
        # Esperar a que el panel de tarifas aparezca (espera al primer tcard)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tcard")))
        # Hacer clic en Comfort
        comfort = self.wait.until(EC.element_to_be_clickable(self.COMFORT_CATEGORY_BUTTON))
        comfort.click()


    # Método para obtener el elemento de la categoría Comfort        
    def get_comfort_element(self):
        # Obtener el elemento de la categoría Comfort
        return self.wait.until(EC.visibility_of_element_located(self.COMFORT_CATEGORY_BUTTON))


    # Método para hacer clic en el campo de teléfono
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


    # Método para ingresar el número de teléfono        
    def enter_phone_number(self, phone):
        """Ingresa el número de teléfono en el campo de entrada"""
        phone_input = self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(phone)

    
    # Método para hacer clic en el botón Siguiente
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


    # Método para hacer clic en el botón Método de pago
    def click_payment_method_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        )
        button.click()
        print("✅ Botón 'Método de pago' clickeado.")
    
    
    # Método para verificar si el botón Método de pago está visible    
    def is_payment_method_button_visible(self):
        try:
            button = self.wait.until(
                EC.visibility_of_element_located(self.PAYMENT_METHOD_BUTTON)
            )
            is_visible = button.is_displayed()
            if is_visible:
                print("✅ Botón 'Método de pago' está visible.")
            return is_visible
        except Exception as e:
            print(f"❌ Botón 'Método de pago' NO está visible: {e}")
            return False


    # Método para hacer click en el botón Agregar tarjeta
    def click_add_card_button(self):
        """Hace clic en el botón 'Agregar tarjeta'"""
        button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_CARD_BUTTON)
        )
        button.click()
        print("✅ Botón 'Agregar tarjeta' clickeado.")


    # Método para verificar que "Agregar tarjeta" esté visible
    def is_add_card_button_visible(self):
        """Verifica que el botón 'Agregar tarjeta' esté visible"""
        try:
            button = self.wait.until(
                EC.visibility_of_element_located(self.ADD_CARD_BUTTON)
            )
            is_visible = button.is_displayed()
            if is_visible:
                print("✅ Botón 'Agregar tarjeta' está visible.")
            return is_visible
        except Exception as e:
            print(f"❌ Botón 'Agregar tarjeta' NO está visible: {e}")
            return False


    # Método para ingresar el número de tarjeta
    def enter_card_number(self, card_number):
        input_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)
        )
        input_field.clear()
        input_field.send_keys(card_number)
        print(f"✅ Número de tarjeta '{card_number}' ingresado.")


    # Método para verificar el valor del campo número de tarjeta
    def get_card_number_value(self):
        """Obtiene el valor del campo número de tarjeta"""
        input_field = self.driver.find_element(*self.CARD_NUMBER_INPUT)
        value = input_field.get_attribute("value")
        print(f"💳 Valor del campo número de tarjeta: '{value}'")
        return value


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