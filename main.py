# Localizadores y Métodos

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdrive
class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
    def set_from_address(self, address):
        from_input = self.driver.find_element(By.ID, "from")
        from_input.clear()
        from_input.send_keys(address)
    def set_to_address(self, address):
        to_input = self.driver.find_element(By.ID, "to")
        to_input.clear()
        to_input.send_keys(address)
    def click_request_taxi(self):
        request_taxi_button = self.driver.find_element(By.XPATH, "//button[text()='Pedir un taxi']")
        request_taxi_button.click()
    def select_category(self, category_name):
        category = self.driver.find_element(By.XPATH, f"//div[text()='{category_name}']")
        category.click()
    def click_phone_field(self):
        phone_field = self.driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
        phone_field.click()
    def enter_phone_number(self, phone):
        phone_input = self.driver.find_element(By.ID, "phone")
        phone_input.clear()
        phone_input.send_keys(phone)
    def click_next_button(self):
        next_button = self.driver.find_element(By.XPATH, "//button[text()='Siguiente']")
        next_button.click()
    def retrieve_sms_code(self):
        # Ir a la pestaña "Network"
        self.driver.get("chrome://devtools")
        # Esperar a que se cargue la pestaña Network
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='tab'][text()='Network']")))
        # Hacer clic en la pestaña "Network"
        network_tab = self.driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
        network_tab.click()

        # Lógica para obtener y confirmar el código SMS
    def select_payment_method(self):
        payment_arrow = self.driver.find_element(By.XPATH, "//img[@alt='Arrow right']")
        payment_arrow.click()

        add_card = self.driver.find_element(By.XPATH, "//div[text()='Agregar una tarjeta']")
        add_card.click()

        # Lógica para agregar la tarjeta de crédito
    def add_comment_for_driver(self, comment):
        comment_input = self.driver.find_element(By.ID, "comment")
        comment_input.clear()
        comment_input.send_keys(comment)
    def activate_blankets_and_tissues(self):
        blankets_button = self.driver.find_element(By.CLASS_NAME, "slider")
        blankets_button.click()
    def add_ice_creams(self):
        ice_cream_button = self.driver.find_element(By.CLASS_NAME, "counter-plus")
        ice_cream_button.click()
        ice_cream_button.click()
    def request_taxi_again(self):
        request_taxi_button = self.driver.find_element(By.CLASS_NAME, "smart-button-main")
        request_taxi_button.click()
    def wait_for_bender(self):
        bender_image = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
        )
    def wait_and_close_page(self, time_to_wait=5):
        time.sleep(time_to_wait)
        self.driver.quit()

# Uso en main.py
if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time

    driver = webdriver.Chrome()
    driver.get("URL_DE_URBAN_ROUTES")

    urban_routes_page = UrbanRoutesPage(driver)

    urban_routes_page.set_from_address("East 2nd Street, 601")
    urban_routes_page.set_to_address("1300 1st St")
    urban_routes_page.click_request_taxi()
    urban_routes_page.select_category("Comfort")

    urban_routes_page.click_phone_field()
    urban_routes_page.enter_phone_number("+12312312312")
    urban_routes_page.click_next_button()

    # Obtener y confirmar código SMS
    urban_routes_page.retrieve_sms_code()
    urban_routes_page.select_payment_method()
    urban_routes_page.add_comment_for_driver("Traer los snacks")
    urban_routes_page.activate_blankets_and_tissues()
    urban_routes_page.add_ice_creams()
    urban_routes_page.request_taxi_again()
    urban_routes_page.wait_for_bender()

    # Esperar y cerrar la página
    urban_routes_page.wait_and_close_page(5)
