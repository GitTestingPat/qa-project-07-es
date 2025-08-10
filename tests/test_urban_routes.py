import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data

@pytest.mark.smoke
def test_01_urbanroutes_flow(driver):
    driver.get(data.BASE_URL)
    assert "Urban Routes" in driver.title

@pytest.mark.smoke
def test_02_set_from_address(driver):
    from_input = driver.find_element(By.ID, "from")
    from_input.clear()
    from_input.send_keys(data.UrbanRoutesData.ADDRESS_FROM)
    assert from_input.get_attribute("value") == data.UrbanRoutesData.ADDRESS_FROM

@pytest.mark.smoke
def test_03_set_to_address(driver):
    to_input = driver.find_element(By.ID, "to")
    to_input.clear()
    to_input.send_keys(data.UrbanRoutesData.TO_ADDRESS)
    assert to_input.get_attribute("value") == data.UrbanRoutesData.TO_ADDRESS

@pytest.mark.smoke
def test_04_click_request_taxi(driver):
    request_taxi_button = driver.find_element(By.XPATH, f"//button[text()='{data.UrbanRoutesData.REQUEST_TAXI}']")
    request_taxi_button.click()
    assert "Comfort" in driver.page_source

@pytest.mark.smoke
def test_05_select_category(driver):
    comfort_category = driver.find_element(By.XPATH, f"//div[text()='{data.UrbanRoutesData.SELECT_CATEGORY}']")
    comfort_category.click()
    assert data.UrbanRoutesData.SELECT_CATEGORY in driver.page_source

@pytest.mark.smoke
def test_06_click_phone_field(driver):
    phone_field = driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
    phone_field.click()
    assert "Número de teléfono" in driver.page_source

@pytest.mark.smoke
def test_07_enter_phone_number(driver):
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.clear()
    phone_input.send_keys(data.UrbanRoutesData.PHONE_NUMBER)
    assert phone_input.get_attribute("value") == data.UrbanRoutesData.PHONE_NUMBER

@pytest.mark.smoke
def test_08_click_next_button(driver):
    next_button = driver.find_element(By.XPATH, "//button[text()='Siguiente']")
    next_button.click()
    assert driver.find_element(By.ID, "code").is_displayed()

@pytest.mark.smoke
def test_09_select_tab(driver):
    network_tab = driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
    network_tab.click()
    assert network_tab.is_displayed()

@pytest.mark.smoke
def test_010_wait_for_network_tab(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='name']/div"))
    )
    assert len(driver.find_elements(By.XPATH, "//div[@class='name']/div")) > 0

@pytest.mark.smoke
def test_011_select_last_network_link(driver):
    network_links = driver.find_elements(By.XPATH, "//div[@class='name']/div")
    last_link = network_links[-1]
    last_link.click()
    assert last_link.is_displayed()

@pytest.mark.smoke
def test_012_wait_for_preview_code(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='preview']/div"))
    )
    assert driver.find_element(By.XPATH, "//div[@class='preview']/div").is_displayed()

@pytest.mark.smoke
def test_013_copy_number(driver):
    code_element = driver.find_element(By.XPATH, "//div[@class='preview']/div")
    verification_code = code_element.text
    assert verification_code != ""

@pytest.mark.smoke
def test_014_enter_number(driver):
    verification_code = data.UrbanRoutesData.VERIFICATION_CODE
    sms_input = driver.find_element(By.ID, "code")
    sms_input.clear()
    sms_input.send_keys(verification_code)
    assert sms_input.get_attribute("value") == verification_code

@pytest.mark.smoke
def test_015_select_button(driver):
    confirm_button = driver.find_element(By.XPATH, "//button[text()='Confirmar']")
    confirm_button.click()
    assert confirm_button.is_displayed()

@pytest.mark.smoke
def test_016_select_arrow(driver):
    payment_arrow = driver.find_element(By.XPATH, "//img[@alt='Arrow right']")
    payment_arrow.click()
    assert payment_arrow.is_displayed()

@pytest.mark.smoke
def test_017_add_card(driver):
    add_card = driver.find_element(By.XPATH, "//div[text()='Agregar una tarjeta']")
    add_card.click()
    assert add_card.is_displayed()

@pytest.mark.smoke
def test_018_enter_number(driver):
    card_number_input = driver.find_element(By.ID, "number")
    card_number_input.clear()
    card_number_input.send_keys(data.UrbanRoutesData.CARD_NUMBER)
    assert card_number_input.get_attribute("value") == data.UrbanRoutesData.CARD_NUMBER

@pytest.mark.smoke
def test_019_enter_code(driver):
    code_input = driver.find_element(By.ID, "code")
    code_input.clear()
    code_input.send_keys(data.UrbanRoutesData.VERIFICATION_CODE)
    assert code_input.get_attribute("value") == data.UrbanRoutesData.VERIFICATION_CODE

@pytest.mark.smoke
def test_020_select_overlay(driver):
    overlay = driver.find_element(By.CLASS_NAME, "overlay")
    overlay.click()
    assert overlay.is_enabled()

@pytest.mark.smoke
def test_021_select_link(driver):
    link_button = driver.find_element(By.XPATH, "//button[text()='Enlace']")
    link_button.click()
    assert link_button.is_displayed()

@pytest.mark.smoke
def test_022_select_close_button(driver):
    close_button = driver.find_element(By.CLASS_NAME, "close-button")
    close_button.click()
    assert close_button.is_displayed()

@pytest.mark.smoke
def test_023_add_text(driver):
    comment_input = driver.find_element(By.ID, "comment")
    comment_input.clear()
    comment_input.send_keys(data.UrbanRoutesData.MESSAGE_FOR_DRIVER)
    assert comment_input.get_attribute("value") == data.UrbanRoutesData.MESSAGE_FOR_DRIVER

@pytest.mark.smoke
def test_024_select_blankets(driver):
    blankets_button = driver.find_element(By.CLASS_NAME, "slider")
    blankets_button.click()
    assert blankets_button.is_selected()

@pytest.mark.smoke
def test_025_add_ice_creams(driver):
    ice_cream_button = driver.find_element(By.CLASS_NAME, "counter-plus")
    ice_cream_button.click()
    ice_cream_button.click()
    # Puedes agregar un assert más específico si hay un contador visible

@pytest.mark.smoke
def test_026_order_taxi_final(driver):
    order_taxi_button = driver.find_element(By.CLASS_NAME, "smart-button-main")
    order_taxi_button.click()
    assert order_taxi_button.is_displayed()

@pytest.mark.smoke
def test_027_wait_for_bender(driver):
    bender_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
    )
    assert bender_image.is_displayed()