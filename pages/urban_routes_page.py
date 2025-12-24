import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Importar utilidades
from utils.network_utils import extract_code_from_sms_request


class UrbanRoutesPage:  
    # Localizador para el campo origen
    FROM_FIELD = (By.XPATH, "//input[@id='from']") 
    
    # Localizador para el campo destino
    TO_FIELD = (By.XPATH, "//input[@id='to']") 
    
    # Localizador para el botón pedir un taxi 
    REQUEST_TAXI_BUTTON = (By.CLASS_NAME, "button.round") 
    
    # Localizador para seleccionar categoria comfort
    COMFORT_OPTION = (By.XPATH, "//div[contains(text(), 'Comfort')]") 

    # Localizador para seleccionar categoria comfort
    COMFORT_CATEGORY_BUTTON = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[normalize-space()='Comfort']]") 
    
    # Localizador para el botón teléfono
    PHONE_NUMBER_BUTTON = (By.XPATH, "//div[contains(text(), 'Phone number')]") 
    
    # Localizador para la etiqueta que está encima del botón de teléfono
    PHONE_LABEL = (By.CSS_SELECTOR, "label[for='phone']")  
    
    # Localizador para ingresar el número de teléfono
    PHONE_INPUT = (By.ID, "phone") 
    
    # Localizador para el botón Siguiente
    NEXT_BUTTON = (By.CSS_SELECTOR, "form button.button.full") 
    
    # Localizador para el campo código de verificación
    SMS_CODE_INPUT = (By.ID, "code") 
    
    # Localizador para el botón Confirmar
    CONFIRM_BUTTON = (By.XPATH, "//button[@class='button full' and @type='submit' and contains(text(), 'Confirm')]") 
    
    # Localizador para el botón Reenviar código
    RESEND_CODE_BUTTON = (By.XPATH, "//button[contains(text(), 'Vuelve a enviar el código')]") 
    
    # Localizador para el botón Método de pago  
    PAYMENT_METHOD_BUTTON = (By.XPATH, "//div[@class='pp-button filled']") 
    
    # Localizador para Agregar tarjeta
    ADD_CARD_BUTTON = (By.XPATH, "//div[@class='pp-title' and text()='Add a card']") 
    
    # Localizador para el campo Número de tarjeta
    CARD_NUMBER_INPUT = (By.ID, "number") 
    
    # Localizador para el campo CVV (código de tarjeta) - Por placeholder
    CARD_CVV_INPUT = (By.XPATH, "//input[@id='code' and @placeholder='12']")    
    
    # Localizador para el botón Agregar tarjeta
    ADD_CARD_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    
    # Localizador para el botón Cerrar modal
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[@class='close-button section-close' or contains(@class, 'payment-picker close')]") 
    
    # Localizador para mensaje al conductor
    DRIVER_MESSAGE_FIELD = (By.ID, "comment") 
    
    # Localizador para la sección Requisitos del Pedido
    ORDER_REQUIREMENTS_SECTION = (By.XPATH, "//div[@class='reqs-head']")
    
    # --- Localizadores para requisitos del pedido ---
    # Localizador para el switch de agregar mantas y pañuelos
    BLANKETS_SWITCH = (By.XPATH, "//div[@class='r-sw']//input[@type='checkbox']")
        
    # Localizador para cortina acústica (checkbox)
    ACOUSTIC_CURTAIN_SWITCH = (By.XPATH, "(//input[@type='checkbox' and @class='switch-input'])[2]")
    
    # Localizador para agregar helados (botón +)
    ICE_CREAM_COUNTER_PLUS = (By.XPATH, "//div[@class='r-group']//div[@class='counter-plus']")
    
    # Localizador para agregar chocolate (botón + de chocolate específicamente)
    CHOCOLATE_COUNTER_PLUS = (By.XPATH, "//div[@class='r-counter-label' and text()='Chocolate']/following-sibling::div[@class='r-counter']//div[@class='counter-plus']")
    
    # Localizador para agregar fresa (botón + de fresa específicamente)
    STRAWBERRY_COUNTER_PLUS = (By.XPATH, "//div[@class='r-counter-label' and text()='Strawberry']/following-sibling::div[@class='r-counter']//div[@class='counter-plus']")
    
    # ---------------------------------------------
    # Localizador para el botón final pedir un taxi 
    ORDER_TAXI_FINAL_BUTTON = (By.CLASS_NAME, "smart-button")

    # Localizador para la imagen del conductor
    DRIVER_IMAGE = (By.XPATH, "//img[@alt]")
    
    # Localizador para el modal de información del conductor
    DRIVER_INFO_MODAL = (By.CLASS_NAME, "order-header-title")
    
    # Botón de detalles del viaje
    TRIP_DETAILS_BUTTON = (By.XPATH, "//img[@alt='burger']")
    
    # Botón cancelar
    CANCEL_BUTTON = (By.XPATH, "//button[@type='button']//img[@alt='close']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    
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
        Obtiene el código SMS del tráfico de red usando CDP.
        
        Esta función usa network_utils para extraer el código.
        
        Args:
            phone_number: Número de teléfono usado
            
        Returns:
            str: Código SMS extraído
        """
        return extract_code_from_sms_request(phone_number, self.driver, timeout=60)


    # Método para hacer clic en el botón Método de pago
    def click_payment_method_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        )
        button.click()
        print("✅ Botón 'Payment method Cash' clickeado.")
    
    
    # Método para verificar si el botón Método de pago está visible    
    def is_payment_method_button_visible(self):
        try:
            button = self.wait.until(
                EC.visibility_of_element_located(self.PAYMENT_METHOD_BUTTON)
            )
            is_visible = button.is_displayed()
            if is_visible:
                print("✅ Botón 'Payment method Cash' está visible.")
            return is_visible
        except Exception as e:
            print(f"❌ Botón 'Payment method' NO está visible: {e}")
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


    # Método para ingresar el código de la tarjeta
    def enter_card_code(self, code):
        cvv_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_CVV_INPUT)
        )
        cvv_field.clear()
        cvv_field.send_keys(code)
        print(f"✅ Código CVV '{code}' ingresado.")

        
    # Método para obtener el valor del campo código CVV (dentro del iframe)
    def get_card_code_value(self):
        cvv_field = self.driver.find_element(*self.CARD_CVV_INPUT)
        value = cvv_field.get_attribute("value")
        print(f"🔢 Valor del código CVV: '{value}'")
        return value
    
    
    # Método para encontrar el botón Agregar y hacer clic en él
    def click_add_card_confirm_button(self):
        """Hace clic en el botón 'Agregar' para confirmar la tarjeta"""
        
        # Activar el modal haciendo clic en el campo número de tarjeta
        try:
            card_number_field = self.driver.find_element(*self.CARD_NUMBER_INPUT)
            card_number_field.click()
            time.sleep(0.3)  # Dar tiempo a que se disparen eventos JS
            print("✅ Modal activado con clic en número de tarjeta.")
        except Exception as e:
            print(f"⚠️ No se pudo hacer clic en número de tarjeta: {e}")
        
        # Esperar y hacer clic en el botón
        button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_CARD_CONFIRM_BUTTON)
        )
        
        # Scroll al botón (por si está fuera de vista)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.2)
        
        # Clic
        button.click()
        print("✅ Botón 'Agregar' clickeado.")        
        
    
    # Método para cerrar el modal de pago
    def close_payment_modal(self):
        """Cierra el modal de pago"""
        try:
            close_button = self.wait.until(
                EC.element_to_be_clickable(self.CLOSE_MODAL_BUTTON)
            )
            close_button.click()
            print("✅ Modal de pago cerrado.")
        except Exception as e:
            print(f"⚠️ No se pudo cerrar el modal: {e}")
            # Intentar con JavaScript
            button = self.driver.find_element(*self.CLOSE_MODAL_BUTTON)
            self.driver.execute_script("arguments[0].click();", button)
            print("✅ Modal cerrado con JavaScript.")
            
    
    # Método para ingresar un mensaje para el conductor        
    def enter_driver_message(self, message):
        """Ingresa un mensaje para el conductor"""
        input_field = self.wait.until(
            EC.visibility_of_element_located(self.DRIVER_MESSAGE_FIELD)
        )
        input_field.clear()
        input_field.send_keys(message)
        print(f"✅ Mensaje para el conductor ingresado: '{message}'")
    
    
    # Método para obtener el valor del campo de mensaje al conductor
    def get_driver_message_value(self):
        """Obtiene el valor del campo de mensaje al conductor"""
        input_field = self.driver.find_element(*self.DRIVER_MESSAGE_FIELD)
        value = input_field.get_attribute("value")
        print(f"💬 Mensaje actual: '{value}'")
        return value
    

    # Método para verificar si la sección de Requisitos del Pedido está visible y hacer clic en ella
    def is_order_requirements_section_visible(self):
        """Verifica si la sección de Requisitos del Pedido está visible"""
        try:
            section = self.wait.until(
                EC.visibility_of_element_located(self.ORDER_REQUIREMENTS_SECTION)
            )
            is_visible = section.is_displayed()
            if is_visible:
                print("✅ Sección 'Requisitos del Pedido' está visible.")
            return is_visible
        except Exception as e:
            print(f"❌ Sección 'Requisitos del Pedido' NO está visible: {e}")
            return False
    
    
    # Método para agregar mantas y pañuelos
    def add_blankets_and_tissues(self):
        """Activa el switch de mantas y pañuelos"""
        import time
        
        # Esperar a que overlay desaparezca completamente
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))
        
        # Localizar y hacer clic con JavaScript directamente
        switch_input = self.wait.until(
            EC.presence_of_element_located(self.BLANKETS_SWITCH)
        )
        
        # Usar JavaScript para evitar problemas de interceptación
        self.driver.execute_script("arguments[0].click();", switch_input)
        print("✅ Switch de mantas y pañuelos activado")
        
    
    # Método para agregar cortina acústica
    def add_acoustic_curtain(self):
        """Activa el switch de cortina acústica"""
        import time
        
        # Esperar a que overlay desaparezca completamente
        time.sleep(1)
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))
        except Exception:
            pass
        
        # Hacer scroll hacia el elemento primero
        self.driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(0.5)
        
        # Localizar el segundo checkbox (cortina acústica)
        switch_input = self.wait.until(
            EC.presence_of_element_located(self.ACOUSTIC_CURTAIN_SWITCH)
        )
        
        # Usar JavaScript para hacer clic
        self.driver.execute_script("arguments[0].click();", switch_input)
        print("✅ Switch de cortina acústica activado")
        
    
    # Método para agregar helados
    def add_ice_cream(self, quantity=2):
        """Agrega helados usando el botón +"""
        import time
        
        # Esperar a que overlay desaparezca completamente
        time.sleep(1)
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))
        except Exception:
            pass
        
        # Hacer scroll hacia el elemento
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.5)
        
        # Localizar el botón +
        plus_button = self.wait.until(
            EC.presence_of_element_located(self.ICE_CREAM_COUNTER_PLUS)
        )
        
        # Hacer clics usando JavaScript para evitar interceptación
        for i in range(quantity):
            self.driver.execute_script("arguments[0].click();", plus_button)
            time.sleep(0.3)
            print(f"✅ Helado agregado ({i+1}/{quantity})")
            
    
    # Método para agregar chocolate
    def add_chocolate(self, quantity=2):
        """Agrega chocolates usando el botón +"""
        import time
        
        # Esperar a que overlay desaparezca completamente
        time.sleep(1)
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))
        except Exception:
            pass
        
        # Hacer scroll hacia el elemento
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(0.5)
        
        # Localizar el botón +
        plus_button = self.wait.until(
            EC.presence_of_element_located(self.CHOCOLATE_COUNTER_PLUS)
        )
        
        # Hacer clics usando JavaScript para evitar interceptación
        for i in range(quantity):
            self.driver.execute_script("arguments[0].click();", plus_button)
            time.sleep(0.3)
            print(f"✅ Chocolate agregado ({i+1}/{quantity})")
            
    # Método para agregar fresa
    def add_strawberry(self, quantity=2):
        """Agrega fresas usando el botón +"""
        import time
        
        # Esperar a que overlay desaparezca completamente
        time.sleep(1)
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))
        except Exception:
            pass
        
        # Hacer scroll hacia el elemento
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(0.5)
        
        # Localizar el botón +
        plus_button = self.wait.until(
            EC.presence_of_element_located(self.STRAWBERRY_COUNTER_PLUS)
        )
        
        # Hacer clics usando JavaScript para evitar interceptación
        for i in range(quantity):
            self.driver.execute_script("arguments[0].click();", plus_button)
            time.sleep(0.3)
            print(f"✅ Fresa agregada ({i+1}/{quantity})")


    # Método para hacer clic en el botón final Pedir un taxi
    def click_order_taxi_button(self):
        """Hace clic en el botón final 'Pedir un taxi'"""
        import time
        
        # Esperar a que overlay desaparezca completamente
        time.sleep(1)
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))
        except Exception:
            pass
        
        # Hacer scroll hacia el botón
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(0.5)
        
        # Localizar el botón
        button = self.wait.until(
            EC.presence_of_element_located(self.ORDER_TAXI_FINAL_BUTTON)
        )
        
        # Hacer clic con JavaScript para evitar interceptación
        self.driver.execute_script("arguments[0].click();", button)
        print("✅ Botón 'Pedir un taxi' clickeado.")
    
    
    # Método para verificar si la imagen del conductor está visible
    def is_driver_image_visible(self, timeout=40):
        """Verifica si la imagen del conductor está visible"""
        try:
            print("⏳ Esperando que aparezca la imagen del conductor...")
            
            # Esperar a que aparezca la imagen del conductor
            image = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.DRIVER_IMAGE)
            )
            
            is_visible = image.is_displayed()
            if is_visible:
                print("✅ Imagen del conductor visible.")
            return is_visible
            
        except Exception as e:
            print(f"❌ Imagen del conductor no encontrada después de {timeout}s: {e}")
            return False
        
    
    # Método para el modal de información del conductor
    def is_driver_info_visible(self): 
        """Verifica si el modal de información del conductor está visible"""
        try:
            modal = self.wait.until(
                EC.visibility_of_element_located(self.DRIVER_INFO_MODAL)
            )
            is_visible = modal.is_displayed()
            if is_visible:
                print("✅ Modal de información del conductor visible.")
            return is_visible
        except Exception as e:
            print(f"❌ Modal de información del conductor NO está visible: {e}")
            return False
    
    
    # Método para hacer clic en el botón Detalles del viaje
    def click_trip_details_button(self):  
        """Hace clic en el botón 'Detalles del viaje'"""
        try:
            # Esperar a que el elemento esté presente
            button = self.wait.until(
                EC.presence_of_element_located(self.TRIP_DETAILS_BUTTON)
            )
            
            # Intentar clic normal primero
            try:
                button.click()
                print("✅ Botón 'Detalles del viaje' clickeado (clic normal).")
                return True
            except Exception:
                # Si falla por overlay, usar JavaScript
                print("⚠️ Clic normal bloqueado, usando JavaScript...")
                self.driver.execute_script("arguments[0].click();", button)
                print("✅ Botón 'Detalles del viaje' clickeado (JavaScript).")
                return True
                
        except Exception as e:
            print(f"❌ No se pudo hacer clic en 'Detalles del viaje': {e}")
            return False
        
        
    # Método para hacer clic en botón cancelar
    def click_cancel_trip_button(self):  
        """Hace clic en el botón 'Cancelar'"""
        try:
            button = self.wait.until(
                EC.presence_of_element_located(self.CANCEL_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", button)
            print("✅ Botón 'Cancelar' clickeado.")
            print("✅ Viaje cancelado correctamente.")
            return True
        except Exception as e:
            print(f"❌ No se pudo cancelar el viaje: {e}")
            return False
    