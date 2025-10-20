# Este archivo contiene pruebas que simulan el flujo completo de usuario en Urban Routes.
# Debido a las limitaciones del entorno de prueba, algunos pasos (como la obtención del código
# de verificación) requieren interactuar con las herramientas de desarrollo del navegador (DevTools).

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.urban_routes_page import UrbanRoutesPage
import data

@pytest.fixture
def page(driver):
    return UrbanRoutesPage(driver)


# Test 01: Abre la URL base y verifica que el título de la página contenga "Urban Routes".
def test_01_urbanroutes_flow(page):
    print(f"\n🔍 Intentando abrir: '{data.BASE_URL}'")
    page.get_page(data.BASE_URL)
    print(f"📄 Título real: '{page.driver.title}'")
    print(f"🌐 URL actual: {page.driver.current_url}")
    assert "Urban" in page.driver.title  

# Test 02: Ingresa la dirección de origen en el campo correspondiente y verifica que el valor del campo coincida con la dirección esperada.
def test_02_set_from_address(page):
    page.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    assert page.is_from_address_set(data.UrbanRoutesData.ADDRESS_FROM)


# Test 03: Ingresa la dirección de destino en el campo correspondiente y verifica que el valor del campo coincida con la dirección esperada.
def test_03_set_to_address(page):
    page.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    assert page.is_to_address_set(data.UrbanRoutesData.TO_ADDRESS)


# Test 04: Hace clic en el botón "Pedir un taxi" y verifica que el texto "Comfort" aparezca en el código fuente de la página.
def test_04_click_request_taxi(page):
    page.click_request_taxi()
    assert "Comfort" in page.driver.page_source


# Test 05: Hace clic en la categoría "Comfort" y verifica que el texto "Comfort" esté presente en el código fuente de la página.
def test_05_select_category(page):
    page.select_comfort_category()
    assert data.UrbanRoutesData.SELECT_CATEGORY in page.driver.page_source


# Test 06: Hace clic en el campo que muestra el texto "Número de teléfono" y verifica que ese texto aparezca en el código fuente de la página.
def test_06_click_phone_field(page):
    page.click_phone_field()
    assert "Número de teléfono" in page.driver.page_source


# Test 07: Ingresa el número de teléfono en el campo correspondiente y verifica que el valor del campo coincida con el número esperado.
def test_07_enter_phone_number(page):
    page.enter_phone_number(data.UrbanRoutesData.PHONE_NUMBER)
    assert page.driver.find_element(*page.PHONE_INPUT).get_attribute("value") == data.UrbanRoutesData.PHONE_NUMBER


# Test 08: Hace clic en el botón "Siguiente" y verifica que el campo de código SMS (con id "code") esté visible.
def test_08_click_next_button(page):
    page.click_next_button()
    assert page.driver.find_element(By.ID, "code").is_displayed()


# Test 09: Hace clic en la pestaña con texto "Network" y verifica que el elemento esté visible.
def test_09_select_tab(driver):
    network_tab = driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
    network_tab.click()
    assert network_tab.is_displayed()


# Test 10: Espera hasta que aparezcan elementos con XPath "//div[@class='name']/div" y verifica que haya al menos uno.
def test_010_wait_for_network_tab(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='name']/div"))
    )
    assert len(driver.find_elements(By.XPATH, "//div[@class='name']/div")) > 0


# Test 11: Obtiene todos los elementos con XPath "//div[@class='name']/div", hace clic en el último y verifica que esté visible.
def test_011_select_last_network_link(driver):
    network_links = driver.find_elements(By.XPATH, "//div[@class='name']/div")
    last_link = network_links[-1]
    last_link.click()
    assert last_link.is_displayed()


# Test 12: Espera hasta que aparezca un elemento con XPath "//div[@class='preview']/div" y verifica que esté visible.
def test_012_wait_for_preview_code(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='preview']/div"))
    )
    assert driver.find_element(By.XPATH, "//div[@class='preview']/div").is_displayed()


# Test 13: Localiza el elemento que contiene el código de verificación y verifica que su texto no esté vacío.
def test_013_copy_number(driver):
    code_element = driver.find_element(By.XPATH, "//div[@class='preview']/div")
    verification_code = code_element.text
    assert verification_code != ""


# Test 14: Ingresa el código de verificación definido en los datos de prueba en el campo de código SMS y verifica que el valor del campo coincida.
def test_014_enter_number(page):
    verification_code = data.UrbanRoutesData.VERIFICATION_CODE
    sms_input = page.driver.find_element(By.ID, "code")
    sms_input.clear()
    sms_input.send_keys(verification_code)
    assert sms_input.get_attribute("value") == verification_code


# Test 15: Hace clic en el botón "Confirmar" y verifica que el botón esté visible.
def test_015_select_button(page):
    confirm_button = page.driver.find_element(By.XPATH, "//button[text()='Confirmar']")
    confirm_button.click()
    assert confirm_button.is_displayed()


# Test 16: Hace clic en la flecha de pago (imagen con alt="Arrow right") y verifica que la imagen esté visible.
def test_016_select_arrow(page):
    payment_arrow = page.driver.find_element(By.XPATH, "//img[@alt='Arrow right']")
    payment_arrow.click()
    assert payment_arrow.is_displayed()


# Test 17: Hace clic en el elemento con texto "Agregar una tarjeta" y verifica que esté visible.
def test_017_add_card(page):
    add_card = page.driver.find_element(By.XPATH, "//div[text()='Agregar una tarjeta']")
    add_card.click()
    assert add_card.is_displayed()


# Test 18: Ingresa el número de tarjeta en el campo correspondiente y verifica que el valor del campo coincida con el número esperado.
def test_018_enter_number(page):
    card_number_input = page.driver.find_element(By.ID, "number")
    card_number_input.clear()
    card_number_input.send_keys(data.UrbanRoutesData.CARD_NUMBER)
    assert card_number_input.get_attribute("value") == data.UrbanRoutesData.CARD_NUMBER


# Test 19: Ingresa el código de verificación en el campo de código de tarjeta y verifica que el valor del campo coincida con el código esperado.
def test_019_enter_code(page):
    code_input = page.driver.find_element(By.ID, "code")
    code_input.clear()
    code_input.send_keys(data.UrbanRoutesData.VERIFICATION_CODE)
    assert code_input.get_attribute("value") == data.UrbanRoutesData.VERIFICATION_CODE


# Test 20: Hace clic en el elemento con clase "overlay" y verifica que esté habilitado.
def test_020_select_overlay(driver):
    overlay = driver.find_element(By.CLASS_NAME, "overlay")
    overlay.click()
    assert overlay.is_enabled()


# Test 21: Hace clic en el botón con texto "Enlace" y verifica que el botón esté visible.
def test_021_select_link(driver):
    link_button = driver.find_element(By.XPATH, "//button[text()='Enlace']")
    link_button.click()
    assert link_button.is_displayed()


# Test 22: Hace clic en el botón con clase "close-button" y verifica que el botón esté visible.
def test_022_select_close_button(driver):
    close_button = driver.find_element(By.CLASS_NAME, "close-button")
    close_button.click()
    assert close_button.is_displayed()


# Test 23: Ingresa un mensaje para el conductor en el campo de comentario y verifica que el valor del campo coincida con el mensaje esperado.
def test_023_add_text(page):
    comment_input = page.driver.find_element(By.ID, "comment")
    comment_input.clear()
    comment_input.send_keys(data.UrbanRoutesData.MESSAGE_FOR_DRIVER)
    assert comment_input.get_attribute("value") == data.UrbanRoutesData.MESSAGE_FOR_DRIVER


# Test 24: Hace clic en el control deslizante de mantas (elemento con clase "slider") y verifica que el elemento esté seleccionado.
def test_024_select_blankets(page):
    blankets_button = page.driver.find_element(By.CLASS_NAME, "slider")
    blankets_button.click()
    assert blankets_button.is_selected()


# Test 25: Hace clic dos veces en el botón para agregar helados (elemento con clase "counter-plus").
def test_025_add_ice_creams(driver):
    ice_cream_button = driver.find_element(By.CLASS_NAME, "counter-plus")
    ice_cream_button.click()
    ice_cream_button.click()


# Test 26: Hace clic en el botón final para pedir un taxi (elemento con clase "smart-button-main") y verifica que el botón esté visible.
def test_026_order_taxi_final(driver):
    order_taxi_button = driver.find_element(By.CLASS_NAME, "smart-button-main")
    order_taxi_button.click()
    assert order_taxi_button.is_displayed()


# Test 27: Espera hasta que aparezca la imagen de Bender (imagen con alt="close") y verifica que esté visible.
def test_027_wait_for_bender(driver):
    bender_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
    )
    assert bender_image.is_displayed()