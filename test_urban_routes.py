# SET DE PRUEBAS

import time
import pytest
from selenium import webdriver
import selenium.webdriver.common.keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_urbanroutes_flow(driver):
    driver.get("BASE_URL")

    # 1. Escribir la dirección "East 2nd Street, 601" en el campo "Desde"
    from_input = driver.find_element(By.ID, "from")
    from_input.clear()
    from_input.send_keys("East 2nd Street, 601")
    assert from_input.get_attribute("value") == "East 2nd Street, 601"

    # 2. Escribir la dirección "1300 1st St" en el campo "Hasta"
    to_input = driver.find_element(By.ID, "to")
    to_input.clear()
    to_input.send_keys("1300 1st St")
    assert to_input.get_attribute("value") == "1300 1st St"

    # 3. Hacer click en el botón "Pedir un taxi"
    request_taxi_button = driver.find_element(By.XPATH, "//button[text()='Pedir un taxi']")
    request_taxi_button.click()
    assert "Tariff Selection" in driver.page_source

    # 4. Seleccionar la categoría "Comfort"
    comfort_category = driver.find_element(By.XPATH, "//div[text()='Comfort']")
    comfort_category.click()
    assert "Comfort" in comfort_category.text

    # 5. Hacer click en el campo "Número de teléfono"
    phone_field = driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
    phone_field.click()
    assert "Número de teléfono" in driver.page_source

    # 6. Introducir un número válido en el campo "Número de teléfono"
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.clear()
    phone_input.send_keys("+12312312312")
    assert phone_input.get_attribute("value") == "+12312312312"

    # 7. Hacer click en el botón "Siguiente"
    next_button = driver.find_element(By.XPATH, "//button[text()='Siguiente']")
    next_button.click()
    assert "Next Page" in driver.title

    # 8. Proceso para obtener y confirmar el código SMS

    # Hacer click en el campo "Número de teléfono"
    phone_field = driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
    phone_field.click()
    assert "Número de teléfono" in driver.page_source

    # Escribir el número de teléfono en el campo correspondiente
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.clear()
    phone_input.send_keys("+12312312312")
    assert phone_input.get_attribute("value") == "+12312312312"

    # Hacer click en el botón "Siguiente"
    next_button = driver.find_element(By.XPATH, "//button[text()='Siguiente']")
    next_button.click()
    WebDriverWait(driver, 10).until(EC.url_contains("number="))
    assert "number=" in driver.current_url

    # Ir a la pestaña "Network" en Chrome
    driver.get("chrome://devtools")
    assert "chrome://devtools" in driver.current_url

    # Hacer click en la pestaña "Network"
    network_tab = driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
    network_tab.click()
    assert network_tab.is_selected()

    # Esperar a que las solicitudes en la pestaña "Network" estén completamente cargadas
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='name']/div"))
    )
    assert len(driver.find_elements(By.XPATH, "//div[@class='name']/div")) > 0

    # Encontrar y hacer click en el último enlace de la columna "Name" en la pestaña "Network"
    network_links = driver.find_elements(By.XPATH, "//div[@class='name']/div")
    last_link = network_links[-1]  # Último enlace
    last_link.click()
    assert last_link.is_selected()

    # Esperar a que aparezca el código en la pestaña "Preview"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='preview']/div"))
    )
    assert driver.find_element(By.XPATH, "//div[@class='preview']/div").is_displayed()

    # Copiar el código de la pestaña "Preview"
    code_element = driver.find_element(By.XPATH, "//div[@class='preview']/div")
    verification_code = code_element.text
    assert verification_code != ""

    # Encontrar el campo para ingresar el código SMS y pegar el código
    sms_input = driver.find_element(By.ID, "codigo_sms")
    sms_input.clear()
    sms_input.send_keys(verification_code)
    assert sms_input.get_attribute("value") == verification_code

    # Hacer click en el botón "Confirmar"
    confirm_button = driver.find_element(By.XPATH, "//button[text()='Confirmar']")
    confirm_button.click()
    assert confirm_button.is_displayed()

    # 9. Hacer click en el campo "Forma de pago" en la flecha derecha
    payment_arrow = driver.find_element(By.XPATH, "//img[@alt='Arrow right']")
    payment_arrow.click()
    assert payment_arrow.is_displayed()

    # 10. Hacer click en "Agregar una tarjeta"
    add_card = driver.find_element(By.XPATH, "//div[text()='Agregar una tarjeta']")
    add_card.click()
    assert add_card.is_displayed()

    # 11. Escribir el número de tarjeta y su código de verificación
    card_number_input = driver.find_element(By.ID, "number")
    card_number_input.clear()
    card_number_input.send_keys("1234 0000 4321 1234")
    assert card_number_input.get_attribute("value") == "1234 0000 4321 1234"

    # Escribir el código de verificación de la tarjeta
    code_input = driver.find_element(By.ID, "code")
    code_input.clear()
    code_input.send_keys("12")
    assert code_input.get_attribute("value") == "12"

    # 12. Hacer click (parte blanca) fuera del cuadro principal para activar el botón "Enlace"
    overlay = driver.find_element(By.CLASS_NAME, "overlay")
    overlay.click()
    assert overlay.is_enabled()

    # Hacer click en el botón "Enlace"
    enlace_button = driver.find_element(By.XPATH, "//button[text()='Enlace']")
    enlace_button.click()
    assert enlace_button.is_displayed()

    # 13. Hacer click en el botón cerrar ventana
    close_button = driver.find_element(By.CLASS_NAME, "close-button")
    close_button.click()
    assert close_button.is_displayed()

    # 14. Agregar comentario para el conductor
    comment_input = driver.find_element(By.ID, "comment")
    comment_input.clear()
    comment_input.send_keys("Traer los snacks")
    assert comment_input.get_attribute("value") == "Traer los snacks"

    # 15. Activar el botón "mantas y pañuelos"
    blankets_button = driver.find_element(By.CLASS_NAME, "slider")
    blankets_button.click()
    assert blankets_button.is_selected()

    # 16. Agregar 2 helados
    ice_cream_button = driver.find_element(By.CLASS_NAME, "counter-plus")
    ice_cream_button.click()
    ice_cream_button.click()
    assert "counter-plus" in driver.page_source

    # 17. Hacer click en el botón "Pedir un taxi"
    request_taxi_button_2 = driver.find_element(By.CLASS_NAME, "smart-button-main")
    request_taxi_button_2.click()
    assert request_taxi_button_2.is_displayed()

    # 18. Esperar a que aparezca la figura de "Bender"
    bender_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
    )
    assert bender_image.is_displayed()

    # 19. Esperar 5 segundos y cerrar la página
    time.sleep(5)
    driver.close()
