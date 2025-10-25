# Este archivo contiene pruebas que simulan el flujo completo de usuario en Urban Routes.
# Debido a las limitaciones del entorno de prueba, algunos pasos (como la obtención del código
# de verificación) requieren interactuar con las herramientas de desarrollo del navegador (DevTools).
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data


# Test 01: Abre la URL base y verifica que el título de la página contenga "Urban Routes".
def test_01_urbanroutes_flow(page):
    print(f"\n🔍 Abriendo página para test 01: '{data.BASE_URL}'")
    page.get_page(data.BASE_URL)
    print(f"📄 Título real: '{page.driver.title}'")
    print(f"🌐 URL actual: {page.driver.current_url}")
    assert "Urban" in page.driver.title  


# Test 02: Ingresa la dirección de origen en el campo correspondiente y verifica que el valor del campo coincida con la dirección esperada.
def test_02_set_from_address(page_with_url):
    print(f"\n🔍 Abriendo página para test 02: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)

    # Lee el valor REAL del campo usando JavaScript
    from_field = page_with_url.wait.until(
        EC.presence_of_element_located(page_with_url.FROM_FIELD)
    )
    valor_real = page_with_url.driver.execute_script("return arguments[0].value;", from_field)
    valor_esperado = data.UrbanRoutesData.ADDRESS_FROM

    # Muestra EXACTAMENTE lo que pasó
    print(f"\n📝 Dirección escrita en el campo 'from': '{valor_real}'")
    print(f"🎯 Dirección esperada:                '{valor_esperado}'")
    print(f"✅ ¿Coinciden? {valor_real == valor_esperado}")

    # Verifica que el valor ingresado sea correcto 
    assert valor_real == valor_esperado


# Test 03: Ingresa la dirección de destino en el campo correspondiente y verifica que el valor del campo coincida con la dirección esperada.
def test_03_set_to_address(page_with_url):
    print(f"\n🔍 Abriendo página para test 03: '{data.BASE_URL}'")
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)

    # Leer el valor REAL del campo 'to' usando JavaScript
    to_field = page_with_url.wait.until(
        EC.presence_of_element_located(page_with_url.TO_FIELD)
    )
    valor_real = page_with_url.driver.execute_script("return arguments[0].value;", to_field)
    valor_esperado = data.UrbanRoutesData.TO_ADDRESS

    # Mostrar en consola
    print(f"\n📝 Dirección escrita en el campo 'to': '{valor_real}'")
    print(f"🎯 Dirección esperada:                 '{valor_esperado}'")
    print(f"✅ ¿Coinciden? {valor_real == valor_esperado}")

    # Verificar
    assert valor_real == valor_esperado


# Test 04: Hace clic en el botón "Pedir un taxi" y verifica que el texto "Comfort" aparezca en el código fuente de la página.
def test_04_click_request_taxi(page_with_url):
    print(f"\n🔍 Abriendo página para test 04: '{data.BASE_URL}'")
    # Precondiciones: llenar origen y destino
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)

    print("\n🖱️  Haciendo clic en 'Pedir un taxi'...")
    page_with_url.click_request_taxi()

    # Verificar que aparece "Comfort"
    comfort_element = page_with_url.wait.until(
        EC.presence_of_element_located(page_with_url.COMFORT_OPTION)
    )
    comfort_text = comfort_element.text
    print(f"✅ Texto encontrado: '{comfort_text}'")
    assert "Comfort" in comfort_text


# Test 05: Hace clic en la categoría "Comfort" y verifica que el texto "Comfort" esté presente en el código fuente de la página.
def test_05_select_category(page_with_url):
    print(f"\n🔍 Abriendo página para test 05: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()

    print("\n🛋️  Seleccionando categoría 'Comfort'...")
    page_with_url.select_comfort_category()

    # Verificar que el elemento esté visible (usando el MISMO localizador)
    comfort_element = page_with_url.get_comfort_element()
    assert comfort_element.is_displayed()
    print("✅ Categoría 'Comfort' visible y seleccionada.")


# Test 06: Hace clic en el campo que muestra el texto "Número de teléfono" y verifica que ese texto aparezca en el código fuente de la página.
def test_06_click_phone_field(page_with_url):
    print(f"\n🔍 Abriendo página para test 06: '{data.BASE_URL}'")
    print("JS enabled?", page_with_url.driver.execute_script("return true;"))
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()

    print("\n🛋️  Seleccionando categoría 'Comfort'...")
    page_with_url.select_comfort_category()
    
    # # 👇 DIAGNÓSTICO DEL DOM 👇
    # print("\n📄 Guardando el código fuente de la página para inspección...")
    # html_source = page_with_url.driver.page_source
    # with open("debug_page_source.html", "w", encoding="utf-8") as f:
    #     f.write(html_source)
    # print("✅ Código fuente guardado en 'debug_page_source.html'. Por favor, ábrelo en un navegador y busca el campo de teléfono.")
    
    # Haz clic en el input real de teléfono
    page_with_url.click_phone_field()
    print("✅ Campo de teléfono seleccionado.")    
    # Verificar que el texto "Phone number" está en el código fuente
    assert "Phone number" in page_with_url.driver.page_source


# Test 07: Ingresa el número de teléfono en el campo correspondiente y verifica que el valor del campo coincida con el número esperado.
def test_07_enter_phone_number(page_with_url):
    print(f"\n🔍 Abriendo página para test 07: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()

    print("\n🛋️  Seleccionando categoría 'Comfort'...")
    page_with_url.select_comfort_category()
    
    # Hacer clic en el campo de teléfono
    page_with_url.click_phone_field()
    print("✅ Campo de teléfono seleccionado.")
    
    # Ingresar el número de teléfono
    page_with_url.enter_phone_number(data.UrbanRoutesData.PHONE_NUMBER)
    print(f"✅ Número de teléfono '{data.UrbanRoutesData.PHONE_NUMBER}' ingresado.")
    
    # Verificar que el valor del campo coincida
    actual_phone = page_with_url.driver.find_element(*page_with_url.PHONE_INPUT).get_attribute("value")
    assert actual_phone == data.UrbanRoutesData.PHONE_NUMBER, f"Expected: {data.UrbanRoutesData.PHONE_NUMBER}, Got: {actual_phone}"


# Test 08: Hace clic en el botón "Siguiente" y verifica que el campo "Introduce el código del SMS" esté visible.
def test_08_click_next_button(page_with_url):
    print(f"\n🔍 Abriendo página para test 08: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()

    print("\n🛋️  Seleccionando categoría 'Comfort'...")
    page_with_url.select_comfort_category()
    
    # Hacer clic en el campo de teléfono
    page_with_url.click_phone_field()
    print("✅ Campo de teléfono seleccionado.")
    
    # Ingresar el número de teléfono
    page_with_url.enter_phone_number(data.UrbanRoutesData.PHONE_NUMBER)
    print(f"✅ Número de teléfono '{data.UrbanRoutesData.PHONE_NUMBER}' ingresado.")
    
    # Hacer clic en el botón "Siguiente"
    page_with_url.click_next_button()
    assert page_with_url.driver.find_element(By.ID, "code").is_displayed()


# Test 09: Captura el código SMS desde la red, lo ingresa y verifica que el código se haya ingresado correctamente.
def test_09_click_next_button(page_with_url):
    print(f"\n🔍 Abriendo página para test 09: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()

    print("\n🛋️  Seleccionando categoría 'Comfort'...")
    page_with_url.select_comfort_category()
    
    # Hacer clic en el campo de teléfono
    page_with_url.click_phone_field()
    print("✅ Campo de teléfono seleccionado.")
    
    # Ingresar el número de teléfono
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    print(f"✅ Número de teléfono '{phone_number}' ingresado.")
    
    # Hacer clic en el botón "Siguiente"
    page_with_url.click_next_button()
    
    # Verificar que el campo de código esté visible
    assert page_with_url.driver.find_element(By.ID, "code").is_displayed()
    print("✅ Campo 'Introduce el código del SMS' está visible.")

    # Capturar y usar el código de verificación
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        # 🔍 DEBUGGING: Ver todos los botones
        #page_with_url.debug_buttons_in_modal()
        page_with_url.click_confirm_button()
        print("✅ Código SMS verificado exitosamente.")
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")


# Test 10: Hace clic en el botón Método de pago y verifica que el botón esté visible.
def test_10_click_payment_method_button(page_with_url):
    print(f"\n🔍 Abriendo página para test 10: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    print("\n🛋️  Seleccionando categoría 'Comfort'...")
    page_with_url.select_comfort_category()
    
    # Ingresar número de teléfono
    page_with_url.click_phone_field()
    print("✅ Campo de teléfono seleccionado.")
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    print(f"✅ Número de teléfono '{phone_number}' ingresado.")
    
    # Confirmar código SMS
    page_with_url.click_next_button()
    assert page_with_url.driver.find_element(By.ID, "code").is_displayed()
    print("✅ Campo 'Introduce el código del SMS' está visible.")
    
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
        print("✅ Código SMS verificado exitosamente.")
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Test 10: Verificar y hacer clic en Método de pago
    print("\n💳 Verificando botón 'Método de pago'...")
    assert page_with_url.is_payment_method_button_visible()
    page_with_url.click_payment_method_button()
    
    print("✅ Test 10 completado exitosamente.")


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