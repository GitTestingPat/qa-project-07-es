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

    # 2. Escribir la dirección "1300 1st St" en el campo "Hasta"
    to_input = driver.find_element(By.ID, "to")
    to_input.clear()
    to_input.send_keys("1300 1st St")

    # 3. Hacer click en el botón "Pedir un taxi"
    request_taxi_button = driver.find_element(By.XPATH, "//button[text()='Pedir un taxi']")
    request_taxi_button.click()

    # 4. Seleccionar la categoría "Comfort"
    comfort_category = driver.find_element(By.XPATH, "//div[text()='Comfort']")
    comfort_category.click()

    # 5. Hacer click en el campo "Número de teléfono"
    phone_field = driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
    phone_field.click()

    # 6. Introducir un número válido en el campo "Número de teléfono"
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.clear()
    phone_input.send_keys("+12312312312")

    # 7. Hacer click en el botón "Siguiente"
    next_button = driver.find_element(By.XPATH, "//button[text()='Siguiente']")
    next_button.click()

    # 8. Proceso para obtener y confirmar el código SMS

    # Hacer click en el campo "Número de teléfono"
    phone_field = driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
    phone_field.click()

    # Escribir el número de teléfono en el campo correspondiente
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.clear()
    phone_input.send_keys("+12312312312")

    # Hacer click en el botón "Siguiente"
    next_button = driver.find_element(By.XPATH, "//button[text()='Siguiente']")
    next_button.click()

    # Ir a la pestaña "Network" en Chrome
    driver.get("chrome://devtools")
    # Hacer click en la pestaña "Network"
    network_tab = driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
    network_tab.click()

    # Esperar a que las solicitudes en la pestaña "Network" estén completamente cargadas
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='name']/div"))
    )

    # Encontrar y hacer click en el último enlace de la columna "Name" en la pestaña "Network"
    network_links = driver.find_elements(By.XPATH, "//div[@class='name']/div")
    last_link = network_links[-1]  # Último enlace
    last_link.click()

    # Esperar a que aparezca el código en la pestaña "Preview"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='preview']/div"))
    )

    # Copiar el código de la pestaña "Preview"
    code_element = driver.find_element(By.XPATH, "//div[@class='preview']/div")
    verification_code = code_element.text

    # Encontrar el campo para ingresar el código SMS y pegar el código
    sms_input = driver.find_element(By.ID, "codigo_sms")
    sms_input.clear()
    sms_input.send_keys(verification_code)

    # Hacer click en el botón "Confirmar"
    confirm_button = driver.find_element(By.XPATH, "//button[text()='Confirmar']")
    confirm_button.click()

    # 9. Hacer click en el campo "Forma de pago" en la flecha derecha
    payment_arrow = driver.find_element(By.XPATH, "//img[@alt='Arrow right']")
    payment_arrow.click()

    # 10. Hacer click en "Agregar una tarjeta"
    add_card = driver.find_element(By.XPATH, "//div[text()='Agregar una tarjeta']")
    add_card.click()

    # 11. Escribir el número de tarjeta y su código de verificación
    card_number_input = driver.find_element(By.ID, "number")
    card_number_input.clear()
    card_number_input.send_keys("1234 0000 4321 1234")

    code_input = driver.find_element(By.ID, "code")
    code_input.clear()
    code_input.send_keys("12")

    # 12. Hacer click fuera del cuadro principal para activar el botón "Enlace"
    overlay = driver.find_element(By.CLASS_NAME, "overlay")
    overlay.click()

    enlace_button = driver.find_element(By.XPATH, "//button[text()='Enlace']")
    enlace_button.click()

    # 13. Hacer click en el botón cerrar ventana
    close_button = driver.find_element(By.CLASS_NAME, "close-button")
    close_button.click()

    # 14. Agregar comentario para el conductor
    comment_input = driver.find_element(By.ID, "comment")
    comment_input.clear()
    comment_input.send_keys("Traer los snacks")

    # 15. Activar el botón "mantas y pañuelos"
    blankets_button = driver.find_element(By.CLASS_NAME, "slider")
    blankets_button.click()

    # 16. Agregar 2 helados
    ice_cream_button = driver.find_element(By.CLASS_NAME, "counter-plus")
    ice_cream_button.click()
    ice_cream_button.click()

    # 17. Hacer click en el botón "Pedir un taxi"
    request_taxi_button_2 = driver.find_element(By.CLASS_NAME, "smart-button-main")
    request_taxi_button_2.click()

    # 18. Esperar a que aparezca la figura de "Bender"
    bender_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
    )

    # 19. Esperar 5 segundos y cerrar la página
    time.sleep(5)
    driver.close()
