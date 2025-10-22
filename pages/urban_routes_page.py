from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    FROM_FIELD = (By.XPATH, "//input[@id='from']")
    TO_FIELD = (By.XPATH, "//input[@id='to']")
    REQUEST_TAXI_BUTTON = (By.CLASS_NAME, "button.round")
    COMFORT_OPTION = (By.XPATH, "//div[contains(text(), 'Comfort')]")
    COMFORT_CATEGORY_BUTTON = (By.XPATH, "//div[@class='tcard-title'][normalize-space()='Comfort']")
    PHONE_FIELD_LABEL = (By.XPATH, "//div[text()='Número de teléfono']")
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Siguiente']")
    SMS_CODE_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirmar']")
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
        self.wait = WebDriverWait(driver, 10)

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
        comfort_button = self.wait.until(
        EC.element_to_be_clickable(self.COMFORT_CATEGORY_BUTTON)
        )
        comfort_button.click()

    def click_phone_field(self):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_FIELD_LABEL)).click()

    def enter_phone_number(self, phone):
        phone_input = self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(phone)

    def click_next_button(self):
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def enter_verification_code(self, code):
        sms_input = self.wait.until(EC.presence_of_element_located(self.SMS_CODE_INPUT))
        sms_input.clear()
        sms_input.send_keys(code)

    def click_confirm_button(self):
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()

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