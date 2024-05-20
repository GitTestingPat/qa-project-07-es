from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import data # Importar el archivo data.py

class UrbanRoutesPage:
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    REQUEST_TAXI_BUTTON = (By.XPATH, "//button[text()='Pedir un taxi']")
    CATEGORY_BUTTON = (By.XPATH, "//div[text()='{}']")
    PHONE_FIELD = (By.XPATH, "//div[text()='Número de teléfono']")
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Siguiente']")
class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    # Escribir la dirección en el Campo "From"
    def set_from_address(self, address):
        from_input = self.driver.find_element(By.ID, "from")
        from_input.clear()
        from_input.send_keys(address)

    # Escribir la dirección en el campo "to"
    def set_to_address(self, address):
        to_input = self.driver.find_element(By.ID, "to")
        to_input.clear()
        to_input.send_keys(address)

    # Hacer click en el botón "Pedir un Taxi"
    def click_request_taxi(self):
        request_taxi_button = self.driver.find_element(By.XPATH, "//button[text()='Pedir un taxi']")
        request_taxi_button.click()

    # Selecionar la categoría "comfort"
    def select_category(self, category_name):
        category = self.driver.find_element(By.XPATH, f"//div[text()='{category_name}']")
        category.click()

    # Hacer click en el campo "número de teléfono"
    def click_phone_field(self):
        phone_field = self.driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
        phone_field.click()

    # Escribir un número de teléfono
    def enter_phone_number(self, phone):
        phone_input = self.driver.find_element(By.ID, "phone")
        phone_input.clear()
        phone_input.send_keys(phone)

    # Hacer click en el botón "Siguiente"
    def click_next_button(self):
        next_button = self.driver.find_element(By.XPATH, "//button[text()='Siguiente']")
        next_button.click()

    # Obtener y confirmar el código SMS
    def retrieve_sms_code(self):
        # Ir a la pestaña "Network"
        self.driver.get("chrome://devtools")
        # Esperar a que se cargue la pestaña Network
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='tab'][text()='Network']")))
        # Hacer clic en la pestaña "Network"
        network_tab = self.driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
        network_tab.click()

    # Agregar una nueva "Tarjeta de Crédito"
    def select_payment_method(self):
        # Hacer click en "Arrow right"
        payment_arrow = self.driver.find_element(By.XPATH, "//img[@alt='Arrow right']")
        payment_arrow.click()
        # Escribir un numero de tarjeta en el campo "Agregar una tarjeta"
        add_card = self.driver.find_element(By.XPATH, "//div[text()='Agregar una tarjeta']")
        add_card.click()

    # Agregar un cometario para el conductor
    def add_comment_for_driver(self, comment):
        comment_input = self.driver.find_element(By.ID, "comment")
        comment_input.clear()
        comment_input.send_keys(comment)

    # Pedir mantas y pañuelos
    def activate_blankets_and_tissues(self):
        blankets_button = self.driver.find_element(By.CLASS_NAME, "slider")
        blankets_button.click()

    # Pedir dos helados
    def add_ice_creams(self):
        ice_cream_button = self.driver.find_element(By.CLASS_NAME, "counter-plus")
        ice_cream_button.click()
        ice_cream_button.click()

    # Hacer click en el botón "Pedir un Taxi"
    def request_taxi_again(self):
        request_taxi_button = self.driver.find_element(By.CLASS_NAME, "smart-button-main")
        request_taxi_button.click()

    # Esperar que aparezca la figura de bender
    def wait_for_bender(self):
        bender_image = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
        )

    # Esperar y cerrar la página
    def wait_and_close_page(self, time_to_wait=5):
        time.sleep(time_to_wait)
        self.driver.quit()

    # Función para configurar el controlador y la página de Urban Routes
    def setup(self):
        driver = webdriver.Chrome()
        driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(driver)
        return driver, urban_routes_page

    # Función para realizar una prueba de reserva de taxi
    def test_booking(self):
        driver, urban_routes_page = setup()
        urban_routes_page.set_from_address(data.ADDRESS_FROM)
        urban_routes_page.set_to_address(data.TO_ADDRESS)
        urban_routes_page.click_request_taxi(data.REQUEST_TAXI)
        urban_routes_page.select_category(data.SELECT_CATEGORY)
        urban_routes_page.enter_phone_number(data.PHONE_NUMBER)
        urban_routes_page.click_next_button()
        assert urban_routes_page.is_phone_submitted(), "Phone number not submitted"
        driver.quit()

    # Función para realizar una prueba de agregar una tarjeta de crédito
    def test_add_credit_card(self):
        driver, urban_routes_page = setup()
        # Agregar una tarjeta de crédito
        urban_routes_page.select_payment_method()
        assert urban_routes_page.is_payment_method_added(), "Payment method not added"
        driver.quit()

    # Función para realizar una prueba de pedido adicional
    def test_additional_order(self):
        driver, urban_routes_page = setup()
        urban_routes_page.add_comment_for_driver("Traer los snacks")
        urban_routes_page.activate_blankets_and_tissues()
        urban_routes_page.add_ice_creams()
        urban_routes_page.request_taxi_again()
        assert urban_routes_page.is_taxi_requested(), "Taxi request failed"
        urban_routes_page.wait_for_bender()
        assert urban_routes_page.wait_for_bender(), "Bender not found"
        driver.quit()

    # Función principal para ejecutar todas las pruebas
    if __name__ == "__main__":
        test_booking()
        test_add_credit_card()
        test_additional_order()

        # Configurar la dirección
        urban_routes_page.set_from_address("East 2nd Street, 601") # Usar la dirección definida en data.py
        urban_routes_page.set_to_address("1300 1st St") # Usar la dirección definida en data.py
        urban_routes_page.click_request_taxi()
        assert urban_routes_page.is_booking_confirmed(), "Booking was not confirmed"

        # seleccionar la tarifa "Confort"
        urban_routes_page.select_category("Comfort")
        assert urban_routes_page.is_category_selected("Comfort"), "Comfort category not selected"

        # Rellenar el número de teléfono
        urban_routes_page.click_phone_field()
        urban_routes_page.enter_phone_number("+12312312312")
        urban_routes_page.click_next_button()
        assert urban_routes_page.is_phone_submitted(), "Phone number not submitted"

        # Obtener y confirmar código SMS
        urban_routes_page.retrieve_sms_code()
        assert sms_code, "SMS code not retrieved successfully"

        # Agregar una tarjeta de Crédito
        urban_routes_page.select_payment_method()
        assert urban_routes_page.is_payment_method_added(), "Payment method not added"

        # Escribir un mensaje para el conductor
        urban_routes_page.add_comment_for_driver("Traer los snacks")
        assert urban_routes_page.is_comment_added("Traer los snacks"), "Comment not added"

        # Pedir una manta y pañuelos.
        urban_routes_page.activate_blankets_and_tissues()
        assert urban_routes_page.are_blankets_activated(), "Blankets not activated"

        # Pedir 2 helados.
        urban_routes_page.add_ice_creams()
        assert urban_routes_page.are_ice_creams_added(), "Ice creams not added"

        # Aparece el modal para buscar un taxi.
        urban_routes_page.request_taxi_again()
        assert urban_routes_page.is_taxi_requested(), "Taxi request failed"

        # Esperar a que aparezca la información del conductor en el modal
        urban_routes_page.wait_for_bender()
        assert urban_routes_page.wait_for_bender(), "Bender not found"

        # Esperar y cerrar la página
        urban_routes_page.wait_and_close_page(5)


