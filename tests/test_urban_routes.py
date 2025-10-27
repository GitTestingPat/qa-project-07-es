# Este archivo contiene pruebas que simulan el flujo completo de usuario en Urban Routes.
# Debido a las limitaciones del entorno de prueba, algunos pasos (como la obtención del código
# de verificación) requieren interactuar con las herramientas de desarrollo del navegador (DevTools).
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data


# Test 01: Abre la URL base y verifica que el título de la página contenga "Urban Routes".
def test_01_urbanroutes_flow(page_with_url):
    print(f"\n🔍 Abriendo página para test 01: '{data.BASE_URL}'")
    page_with_url.get_page(data.BASE_URL)
    print(f"📄 Título real: '{page_with_url.driver.title}'")
    print(f"🌐 URL actual: {page_with_url.driver.current_url}")
    assert "Urban" in page_with_url.driver.title  


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


# Test 11: Hace clic en el elemento "Agregar tarjeta" y verifica que esté visible.
def test_11_click_add_card_button(page_with_url):
    print(f"\n🔍 Abriendo página para test 11: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    print("\n🛋️  Seleccionando categoría 'Comfort'...")
    page_with_url.select_comfort_category()
    
    page_with_url.click_phone_field()
    print("✅ Campo de teléfono seleccionado.")
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    print(f"✅ Número de teléfono '{phone_number}' ingresado.")
    
    page_with_url.click_next_button()
    assert page_with_url.driver.find_element(By.ID, "code").is_displayed()
    print("✅ Campo 'Introduce el código del SMS' está visible.")
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
        print("✅ Código SMS verificado exitosamente.")
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Hacer clic en Método de pago
    page_with_url.click_payment_method_button()
    print("✅ Botón 'Método de pago' clickeado.")
    
    # 🔍 DEBUGGING: Ver elementos disponibles
    # page_with_url.debug_add_card_elements()
    
    # Test 11: Verificar y hacer clic en Agregar tarjeta
    print("\n💳 Verificando botón 'Agregar tarjeta'...")
    assert page_with_url.is_add_card_button_visible()
    page_with_url.click_add_card_button()
    
    print("✅ Test 11 completado exitosamente.")


# Test 12: Ingresa el número de tarjeta en el campo correspondiente y verifica que el valor del campo coincida con el número esperado.
def test_012_enter_number(page):
    card_number_input = page.driver.find_element(By.ID, "number")
    card_number_input.clear()
    card_number_input.send_keys(data.UrbanRoutesData.CARD_NUMBER)
    assert card_number_input.get_attribute("value") == data.UrbanRoutesData.CARD_NUMBER


# Test 13: Ingresa el código de verificación en el campo de código de tarjeta y verifica que el valor del campo coincida con el código esperado.
def test_013_enter_code(page):
    code_input = page.driver.find_element(By.ID, "code")
    code_input.clear()
    code_input.send_keys(data.UrbanRoutesData.VERIFICATION_CODE)
    assert code_input.get_attribute("value") == data.UrbanRoutesData.VERIFICATION_CODE


# Test 14: Hace clic en el botón Agregar.
def test_014_click_add(driver):
    add_button = driver.find_element(By.XPATH, "//button[text()='Agregar']")
    add_button.click()
    assert add_button.is_enabled()


# Test 15: Hace clic en el botón cerrar modal (x).
def test_015_click_close_modal(driver):
    close_button = driver.find_element(By.XPATH, "//button[contains(@class, 'close-button')]")
    close_button.click()
    assert close_button.is_displayed()


# Test 16: Agregar mensaje para el conductor y verifica que el campo "Mensaje para el conductor" esté visible.
def test_016_add_driver_message(driver):
    driver_message_input = driver.find_element(By.ID, "comment")
    driver_message_input.click()
    assert driver_message_input.is_displayed()


# Test 17: Hace clic en el campo "Requisitos del Pedido" y verifica que esté visible.
def test_017_select_order_requirements(page):
    order_requirements_field = page.driver.find_element(By.ID, "order-requirements")
    order_requirements_field.click()
    assert order_requirements_field.is_displayed()


# Test 18: Hace clic en el botón seleccionar "Manta y Pañuelos" y verifica que el botón esté visible..
def test_018_add_blankets_and_tissues(driver):
    blankets_button = driver.find_element(By.CLASS_NAME, "counter-plus")
    blankets_button.click()
    blankets_button.click()


# Test 19: Hace clic en el botón seleccionar "Cortina Acústica" y verifica que el botón esté visible.
def test_019_order_acoustic_curtain(driver):
    order_acoustic_curtain_button = driver.find_element(By.CLASS_NAME, "smart-button-main")
    order_acoustic_curtain_button.click()
    assert order_acoustic_curtain_button.is_displayed()

# <---- Acciones dentro de Cubeta de Helado --->
# Test 20: Hace click en el selector de cantidad de Helado y agrega 1 producto
def test_020_add_ice_cream(driver):
    ice_cream_bucket = driver.find_element(By.CLASS_NAME, "ice-cream-bucket")
    ice_cream_bucket.click()
    quantity_selector = driver.find_element(By.CLASS_NAME, "quantity-selector")
    quantity_selector.click()
    quantity_selector.send_keys("1")
    assert quantity_selector.get_attribute("value") == "1"
    
# Test 21: Hace click en el selector de cantidad de Chocolate y agrega 1 producto

# Test 22: Hace click en el selector de cantidad de Fresa y agrega 1 producto

# Test 23: Hace click en el botón "Pedir un Taxi"


# Test 24: Espera hasta que aparezca la imagen del conductor en el modal y verifica que esté visible.
def test_024_wait_for_conductor_image(driver):
    conductor_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
    )
    assert conductor_image.is_displayed()
    
# Test 25: Hace click en el botón Detalles para ver la información del viaje 

# Test 26: Hace click en el botón "Cancelar"
