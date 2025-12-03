# Este archivo contiene pruebas que simulan el flujo completo de usuario en Urban Routes.
# Debido a las limitaciones del entorno de prueba, algunos pasos (como la obtención del código
# de verificación) requieren interactuar con las herramientas de desarrollo del navegador (DevTools).

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import data


# Test 01: Abre la URL base y verifica que el título de la página contenga "Urban Routes".
def test_01_urbanroutes_flow(page_with_url):
    print(f"\n🔍 Abriendo página para test 01: '{data.BASE_URL}'")
    print(f"📄 Título real: '{page_with_url.driver.title}'")
    print(f"🌐 URL actual: {page_with_url.driver.current_url}")
    
    # Validaciones adicionales
    assert page_with_url.driver.title != "", "❌ El título de la página está vacío"
    assert len(page_with_url.driver.title) > 0, "❌ El título no tiene contenido"
    assert page_with_url.driver.current_url == data.BASE_URL, f"❌ URL no coincide. Esperado: {data.BASE_URL}, Actual: {page_with_url.driver.current_url}"
    assert "Urban" in page_with_url.driver.title, f"❌ 'Urban' no encontrado en título: '{page_with_url.driver.title}'"
    
    # Verificación final
    assert "Urban" in page_with_url.driver.title
    print("✅ Título de la página contiene 'Urban'.")


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

    # Validaciones adicionales
    assert valor_real != "", "❌ El campo 'from' está vacío"
    assert valor_real.strip() != "", "❌ El campo 'from' contiene solo espacios"
    assert valor_real == valor_esperado, f"❌ Dirección no coincide. Esperado: '{valor_esperado}', Obtenido: '{valor_real}'"
    assert from_field.is_displayed(), "❌ El campo 'from' no está visible"
    
    # Verifica que el valor ingresado sea correcto 
    assert valor_real == valor_esperado
    print("✅ Valor ingresado en el campo 'from' es correcto.")


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

    # Validaciones adicionales
    assert valor_real != "", "❌ El campo 'to' está vacío"
    assert valor_real.strip() != "", "❌ El campo 'to' contiene solo espacios"
    assert valor_real == valor_esperado, f"❌ Dirección no coincide. Esperado: '{valor_esperado}', Obtenido: '{valor_real}'"
    assert to_field.is_displayed(), "❌ El campo 'to' no está visible"
    
    # Verifica que el valor ingresado sea correcto
    assert valor_real == valor_esperado
    print("✅ Valor ingresado en el campo 'to' es correcto.")


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
    
    # Validaciones adicionales
    assert comfort_element is not None, "❌ Elemento 'Comfort' no encontrado"
    assert comfort_text != "", "❌ El texto de 'Comfort' está vacío"
    assert comfort_text.strip() != "", "❌ El texto de 'Comfort' contiene solo espacios"
    assert "Comfort" in comfort_text, f"❌ 'Comfort' no encontrado en: '{comfort_text}'"
    assert comfort_element.is_displayed(), "❌ Elemento 'Comfort' no está visible"
    
    print(f"✅ Texto encontrado: '{comfort_text}'")
    
    # Verifica que el texto "Comfort" esté presente
    assert "Comfort" in comfort_text
    print("✅ 'Comfort' encontrado en el código fuente de la página.")
    

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
    
    # Validaciones mejoradas
    assert comfort_element is not None, "❌ Elemento 'Comfort' es None"
    assert comfort_element.is_displayed(), "❌ Elemento 'Comfort' no está visible"
    assert comfort_element.is_enabled(), "❌ Elemento 'Comfort' no está habilitado"
    
    # Verificar atributos CSS para validar selección
    class_attribute = comfort_element.get_attribute("class")
    assert class_attribute is not None, "❌ No se pudo obtener el atributo 'class'"
    assert "tcard" in class_attribute, f"❌ Clase 'tcard' no encontrada en: '{class_attribute}'"
    
    # Verificar visibilidad
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
    
    # Hacer clic en el input real de teléfono
    page_with_url.click_phone_field()
    print("✅ Campo de teléfono seleccionado.")   
    
    # Verificar que el texto "Phone number" está en el código fuente
    assert page_with_url.is_phone_number_in_page_source(), "❌ Validación de página source falló"
    assert page_with_url.is_phone_input_visible_and_enabled() is not None, "❌ Validación del campo teléfono falló"
    
    # Validaciones adicionales
    page_source = page_with_url.driver.page_source
    assert page_source is not None, "❌ El código fuente de la página es None"
    assert len(page_source) > 0, "❌ El código fuente de la página está vacío"
    assert "Phone number" in page_source, "❌ 'Phone number' no encontrado en el código fuente"
    
    phone_input = page_with_url.driver.find_element(*page_with_url.PHONE_INPUT)
    assert phone_input.is_displayed(), "❌ El campo de teléfono no está visible"
    assert phone_input.is_enabled(), "❌ El campo de teléfono no está habilitado"
    
    print("✅ 'Número de teléfono' encontrado en el código fuente de la página.")


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

    # Validaciones adicionales
    assert actual_phone is not None, "❌ El valor del campo teléfono es None"
    assert actual_phone != "", "❌ El campo teléfono está vacío"
    assert actual_phone.strip() != "", "❌ El campo teléfono contiene solo espacios"
    assert len(actual_phone) > 0, "❌ El número de teléfono no tiene dígitos"
    assert actual_phone == data.UrbanRoutesData.PHONE_NUMBER, f"❌ Teléfono no coincide. Esperado: {data.UrbanRoutesData.PHONE_NUMBER}, Obtenido: {actual_phone}"

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
    page_with_url.driver.find_element(By.ID, "code").is_displayed()

    # Validaciones adicionales
    sms_input = page_with_url.driver.find_element(By.ID, "code")
    assert sms_input is not None, "❌ Campo SMS es None"
    assert sms_input.is_displayed(), "❌ Campo 'Introduce el código del SMS' no está visible"
    assert sms_input.is_enabled(), "❌ Campo SMS no está habilitado"
    assert sms_input.get_attribute("type") == "text", "❌ El tipo de campo SMS no es 'text'"
    
    
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
        page_with_url.click_confirm_button()
        print("✅ Código SMS verificado exitosamente.")
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")

        # Validaciones adicionales
    sms_input_value = page_with_url.driver.find_element(By.ID, "code").get_attribute("value")
    assert sms_input_value is not None, "❌ El valor del campo de código SMS es None"
    assert sms_input_value != "", "❌ El campo de código SMS está vacío"
    assert len(sms_input_value) > 0, "❌ El campo de código SMS no contiene dígitos"
    assert sms_input_value.strip() != "", "❌ El campo de código SMS contiene solo espacios"
    assert sms_input_value == sms_code, f"❌ El código ingresado no coincide. Esperado: '{sms_code}', Actual: '{sms_input_value}'"

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
    page_with_url.is_payment_method_button_visible()
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
    
    # Test 11: Verificar y hacer clic en Agregar tarjeta
    print("\n💳 Verificando botón 'Agregar tarjeta'...")
    page_with_url.is_add_card_button_visible()
    page_with_url.click_add_card_button()
    
    print("✅ Test 11 completado exitosamente.")


# Test 12: Ingresa el número de tarjeta en el campo Número de tarjeta y verifica que el valor coincida con el número esperado.
def test_12_enter_card_number(page_with_url):
    print(f"\n🔍 Abriendo página para test 12: '{data.BASE_URL}'")
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
    
    # Hacer clic en Agregar tarjeta
    page_with_url.click_add_card_button()
    print("✅ Botón 'Agregar tarjeta' clickeado.")
    
    # Test 12: Ingresar número de tarjeta y verificar
    print("\n💳 Ingresando número de tarjeta...")
    card_number = data.UrbanRoutesData.CARD_NUMBER
    page_with_url.enter_card_number(card_number)
    
    # Verificar que el valor coincida
    actual_value = page_with_url.get_card_number_value()
    assert actual_value == card_number, f"❌ El número de tarjeta no coincide. Esperado: '{card_number}', Actual: '{actual_value}'"
    
    # Validaciones adicionales
    assert actual_value is not None, "❌ El valor de la tarjeta es None"
    assert actual_value != "", "❌ El campo de tarjeta está vacío"
    assert len(actual_value) > 0, "❌ El número de tarjeta no tiene dígitos"
    assert actual_value.strip() != "", "❌ El campo de tarjeta contiene solo espacios"
    assert actual_value == data.UrbanRoutesData.CARD_NUMBER, f"❌ El número de tarjeta no coincide. Esperado: '{data.UrbanRoutesData.CARD_NUMBER}', Actual: '{actual_value}'"
    
    print("✅ Test 12 completado exitosamente.")


# Test 13: Ingresa el código de verificación en el campo de código de tarjeta y verifica que el valor coincida con el código esperado.
def test_013_enter_code(page_with_url):
    print(f"\n🔍 Abriendo página para test 13: '{data.BASE_URL}'")
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
    
    # Hacer clic en Agregar tarjeta
    page_with_url.click_add_card_button()
    print("✅ Botón 'Agregar tarjeta' clickeado.")
    
    # Ingresar número de tarjeta
    print("\n💳 Ingresando número de tarjeta...")
    card_number = data.UrbanRoutesData.CARD_NUMBER
    page_with_url.enter_card_number(card_number)
    print("✅ Número de tarjeta ingresado.")
    
    # Test 13: Ingresar código CVV y verificar
    print("\n🔢 Ingresando código CVV...")
    card_code = data.UrbanRoutesData.CARD_CODE
    page_with_url.enter_card_code(card_code)
    
    # Verificar que el valor coincida
    actual_code = page_with_url.get_card_code_value()
    assert actual_code == card_code, f"❌ El código CVV no coincide. Esperado: '{card_code}', Actual: '{actual_code}'"
    
    print("✅ Test 13 completado exitosamente.")


# Test 14: Hace clic en el botón "Agregar" para confirmar la tarjeta
def test_014_click_add_card_confirm(page_with_url):
    print(f"\n🔍 Abriendo página para test 14: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Agregar tarjeta
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    
    # page_with_url.debug_iframes()
    
    # Test 14: Hacer clic en Agregar
    print("\n💳 Haciendo clic en 'Agregar'...")
    page_with_url.click_add_card_confirm_button()
    
    print("✅ Test 14 completado exitosamente.")


# Test 15: Hace clic en el botón cerrar modal (x).
def test_015_close_payment_modal(page_with_url):
    print(f"\n🔍 Abriendo página para test 15: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Agregar tarjeta completa
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    
    # Test 15: Cerrar modal
    print("\n❌ Cerrando modal de pago...")
    page_with_url.close_payment_modal()
    
    print("✅ Test 15 completado exitosamente.")


# Test 16: Agregar mensaje para el conductor y verifica que el campo "Mensaje para el conductor" esté visible.
def test_016_enter_driver_message(page_with_url):
    print(f"\n🔍 Abriendo página para test 16: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    # Test 16: Ingresar mensaje para el conductor
    print("\n💬 Ingresando mensaje para el conductor...")
    message = data.UrbanRoutesData.DRIVER_MESSAGE
    page_with_url.enter_driver_message(message)
    
    # Verificar que el mensaje se ingresó correctamente
    actual_message = page_with_url.get_driver_message_value()
    assert actual_message == message, f"❌ El mensaje no coincide. Esperado: '{message}', Actual: '{actual_message}'"
    
    # Validaciones adicionales
    assert actual_message is not None, "❌ El mensaje es None"
    assert actual_message != "", "❌ El campo de mensaje está vacío"
    assert actual_message.strip() != "", "❌ El campo de mensaje contiene solo espacios"
    assert len(actual_message) > 0, "❌ El mensaje no tiene contenido"

    print("✅ Test 16 completado exitosamente.")


# Test 17: Hace clic en el campo "Requisitos del Pedido" y verifica que esté visible.
def test_017_verify_order_requirements_section(page_with_url):
    print(f"\n🔍 Abriendo página para test 17: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    page_with_url.select_comfort_category()
    
    # Este test verifica que la sección de Requisitos del Pedido esté visible
    # Solo confirma que llegamos hasta aquí
    print("\n📋 Verificando sección 'Requisitos del Pedido'...")
    assert page_with_url.is_order_requirements_section_visible()
    
    print("✅ Test 17 completado exitosamente.")


# Test 18: Hace clic en el botón seleccionar "Manta y Pañuelos" y verifica que el botón esté visible..
def test_018_add_blankets_and_tissues(page_with_url):
    print(f"\n🔍 Abriendo página para test 18: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    print("\n📋 Verificando sección 'Requisitos del Pedido'...")
    page_with_url.is_order_requirements_section_visible()
    
    # Test 18: Activar switch de mantas y pañuelos
    print("\n🧣 Activando mantas y pañuelos...")
    page_with_url.add_blankets_and_tissues() 
    
    print("✅ Test 18 completado exitosamente.")


# Test 19: Hace clic en el botón seleccionar "Cortina Acústica" y verifica que el botón esté visible.
def test_019_add_acoustic_curtain(page_with_url):
    print(f"\n🔍 Abriendo página para test 19: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    print("\n📋 Verificando sección 'Requisitos del Pedido'...")
    page_with_url.is_order_requirements_section_visible()
    
    # Test 19: Activar switch de cortina acústica
    print("\n🔇 Activando cortina acústica...")
    page_with_url.add_acoustic_curtain()
    
    print("✅ Test 19 completado exitosamente.")

# <---- Acciones dentro de Cubeta de Helado --->
# Test 20: Hace click en el selector de cantidad de Helado y agrega 1 producto
def test_020_add_ice_cream(page_with_url):
    print(f"\n🔍 Abriendo página para test 20: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    print("\n📋 Verificando sección 'Requisitos del Pedido'...")
    page_with_url.is_order_requirements_section_visible()
    
    # Test 20: Agregar helado
    print("\n🍦 Agregando helado...")
    page_with_url.add_ice_cream(quantity=1)
    
    print("✅ Test 20 completado exitosamente.")
    
    
# Test 21: Hace click en el selector de cantidad de Chocolate y agrega 1 producto
def test_021_add_chocolate(page_with_url):
    print(f"\n🔍 Abriendo página para test 21: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    print("\n📋 Verificando sección 'Requisitos del Pedido'...")
    page_with_url.is_order_requirements_section_visible()
    
    # Test 21: Agregar chocolate
    print("\n🍫 Agregando chocolate...")    
    page_with_url.add_chocolate(quantity=1)
    
    print("✅ Test 21 completado exitosamente.")


# Test 22: Hace click en el selector de cantidad de Fresa y agrega 1 producto
def test_022_add_strawberry(page_with_url):
    print(f"\n🔍 Abriendo página para test 22: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    print("\n📋 Verificando sección 'Requisitos del Pedido'...")
    page_with_url.is_order_requirements_section_visible()
    
    # Test 22: Agregar fresa
    print("\n🍓 Agregando fresa...")
    page_with_url.add_strawberry(quantity=1)
    
    print("✅ Test 22 completado exitosamente.")


# Test 23: Hace click en el botón "Pedir un Taxi"
def test_023_click_order_taxi_final(page_with_url):
    print(f"\n🔍 Abriendo página para test 23: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    # Agregar extras
    page_with_url.add_blankets_and_tissues()
    page_with_url.add_ice_cream(quantity=1)
    
    # Test 23: Pedir un taxi
    print("\n🚕 Haciendo clic en 'Pedir un taxi'...")
    page_with_url.click_order_taxi_button()
    
    print("✅ Test 23 completado exitosamente.")
    

# Test 24: Espera hasta que aparezca la imagen del conductor en el modal y verifica que esté visible.
def test_024_wait_for_driver_image(page_with_url):
    print(f"\n🔍 Abriendo página para test 24: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    # Agregar extras
    page_with_url.add_blankets_and_tissues()
    page_with_url.add_ice_cream(quantity=1)
    
    # Pedir taxi
    page_with_url.click_order_taxi_button()
    
    # Test 24: Esperar imagen del conductor
    is_visible = page_with_url.is_driver_image_visible()
    assert is_visible is True, "❌ La imagen del conductor no está visible"
    
    # Validaciones adicionales
    driver_image = page_with_url.driver.find_element(*page_with_url.DRIVER_IMAGE)
    assert driver_image is not None, "❌ Elemento de imagen es None"
    assert driver_image.get_attribute("alt") is not None, "❌ La imagen no tiene atributo 'alt'"
    assert len(driver_image.get_attribute("alt")) > 0, "❌ El atributo 'alt' de la imagen está vacío"
    
    print("✅ Test 24 completado exitosamente.")
    
    
# Test 25: Verifica información del conductor: nombre, calificación y matrícula del vehículo.
def test_025_verify_driver_info(page_with_url):
    print(f"\n🔍 Abriendo página para test 25: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    # Agregar extras
    page_with_url.add_blankets_and_tissues()
    page_with_url.add_ice_cream(quantity=1)
    
    # Pedir taxi
    page_with_url.click_order_taxi_button()
    
    # Test 25: Verificar info del conductor
    print("\n📝 Verificando información del conductor...")
    assert page_with_url.is_driver_info_visible()
    
    print("✅ Test 25 completado exitosamente.")
    
    
# Test 26: Hace click en el botón Detalles para ver la información del viaje 
def test_026_view_trip_details(page_with_url):
    print(f"\n🔍 Abriendo página para test 26: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    # Agregar extras
    page_with_url.add_blankets_and_tissues()
    page_with_url.add_ice_cream(quantity=1)
    
    # Pedir taxi
    page_with_url.click_order_taxi_button()
    
    # Test 26: Click en Detalles
    print("\n📄 Haciendo clic en 'Detalles' del viaje...")
    assert page_with_url.click_trip_details_button()
    
    print("✅ Test 26 completado exitosamente.")

@pytest.mark.smoke
# Test 27: Hace click en el botón "Cancelar"
def test_027_cancel_trip(page_with_url):
    print(f"\n🔍 Abriendo página para test 27: '{data.BASE_URL}'")
    page_with_url.set_from_address(data.UrbanRoutesData.ADDRESS_FROM)
    page_with_url.set_to_address(data.UrbanRoutesData.TO_ADDRESS)
    page_with_url.click_request_taxi()
    
    page_with_url.select_comfort_category()
    page_with_url.click_phone_field()
    
    phone_number = data.UrbanRoutesData.PHONE_NUMBER
    page_with_url.enter_phone_number(phone_number)
    page_with_url.click_next_button()
    
    # Confirmar SMS
    try:
        sms_code = page_with_url.get_sms_code_from_network(phone_number)
        page_with_url.enter_sms_code(sms_code)
        page_with_url.click_confirm_button()
    except Exception as e:
        pytest.fail(f"❌ Error al capturar o ingresar el código SMS: {e}")
    
    # Configurar pago
    page_with_url.click_payment_method_button()
    page_with_url.click_add_card_button()
    page_with_url.enter_card_number(data.UrbanRoutesData.CARD_NUMBER)
    page_with_url.enter_card_code(data.UrbanRoutesData.CARD_CODE)
    page_with_url.click_add_card_confirm_button()
    page_with_url.close_payment_modal()
    
    # Agregar extras
    page_with_url.add_blankets_and_tissues()
    page_with_url.add_ice_cream(quantity=1)
    
    # Pedir taxi
    page_with_url.click_order_taxi_button()
    
    # Test 27: Cancelar viaje
    print("\n❌ Haciendo clic en 'Cancelar' el viaje...")
    assert page_with_url.click_cancel_trip_button()
        
    print("✅ Test 27 completado exitosamente..")
    

#--- Fin de tests en tests/test_urban_routes.py ---


# TODO: AGREGAR DECORADORES DE ETIQUETAS A CADA TEST
# Ejemplo:
# @pytest.mark.smoke
# def test_01_urbanroutes_flow(page_with_url):
#     ...   
# TODO: AGREGAR MANEJO DE EXCEPCIONES Y LOGGING MÁS DETALLADO SI ES NECESARIO