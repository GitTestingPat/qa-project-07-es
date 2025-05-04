import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import data  # Import file data.py

@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")  # Disable notifications
    options.add_argument("--disable-infobars")       # Disable Chrome's information bar
    options.add_argument("--disable-extensions")     # Disable extensions
    options.add_argument("--start-maximized")        # Start the browser maximized
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_example(browser):
    browser.get(data.BASE_URL)  # Use URL data.py
    assert "Urban Routes" in browser.title  # Replace with the expected page title

@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome() as driver:
        yield driver

# Test 01: Verify that the home page loads correctly
@pytest.mark.smoke
def test_01_urbanroutes_flow(driver):
    driver.get(data.BASE_URL)  # Use URL data.py
    assert "Urban Routes" in driver.title

# Test 02: Write the adress "East 2nd Street, 601" in the field "from"
@pytest.mark.smoke
def test_02_set_from_address(driver):
    from_input = driver.find_element(By.ID, "from")
    from_input.clear()
    from_input.send_keys(data.UrbanRoutesData.ADDRESS_FROM)  # Use URL data.py
    assert from_input.get_attribute("value") == data.UrbanRoutesData.ADDRESS_FROM

# Test 03: Write the adress "1300 1st St" in the field "to"
@pytest.mark.smoke
def test_03_set_to_address(driver):
    to_input = driver.find_element(By.ID, "to")
    to_input.clear()
    to_input.send_keys(data.UrbanRoutesData.TO_ADDRESS)  # Use URL data.py
    assert to_input.get_attribute("value") == data.UrbanRoutesData.TO_ADDRESS

# Test 04. Click in botton "Pedir un taxi"
@pytest.mark.smoke
def test_04_click_request_taxi(driver):
    request_taxi_button = driver.find_element(By.XPATH, f"//button[text()='{data.UrbanRoutesData.REQUEST_TAXI}']")
    request_taxi_button.click()
    assert "Tariff Selection" in driver.page_source

# Test 05: Select category "Comfort"
@pytest.mark.smoke
def test_05_select_category(driver):
    comfort_category = driver.find_element(By.XPATH, f"//div[text()='{data.UrbanRoutesData.SELECT_CATEGORY}']")
    comfort_category.click()
    assert data.UrbanRoutesData.SELECT_CATEGORY in comfort_category.text

# Test 06: Click in the field "Número de teléfono" 
@pytest.mark.smoke
def test_06_click_phone_field(driver):
    phone_field = driver.find_element(By.XPATH, "//div[text()='Número de teléfono']")
    phone_field.click()
    assert "Número de teléfono" in driver.page_source

# Test 07: Add a valid number in the field "Número de teléfono"
@pytest.mark.smoke
def test_07_enter_phone_number(driver):
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.clear()
    phone_input.send_keys(data.UrbanRoutesData.PHONE_NUMBER)  # Use phone number of data.py
    assert phone_input.get_attribute("value") == data.UrbanRoutesData.PHONE_NUMBER

# Test 08: Click in botton "Siguiente"
@pytest.mark.smoke
def test_08_click_next_button(driver):
    next_button = driver.find_element(By.XPATH, "//button[text()='Siguiente']")
    next_button.click()
    assert "Next Page" in driver.title

# Test 09: Click "Network" tab into the real page instead of chrome://devtools
@pytest.mark.smoke
def test_09_select_tab(driver):
    driver.get(data.BASE_URL)  # Change this to the actual URL where the “Network” tab is located.
    network_tab = driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
    network_tab.click()
    assert network_tab.is_selected()

# Test 010: Wait for the “Network” tab to load completely.
@pytest.mark.smoke
def test_010_wait_for_network_tab(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='name']/div"))
    )
    assert len(driver.find_elements(By.XPATH, "//div[@class='name']/div")) > 0

# Test 011: Select the last link in the “Name” column in the “Network” tab.
@pytest.mark.smoke
def test_011_select_last_network_link(driver):
    network_links = driver.find_elements(By.XPATH, "//div[@class='name']/div")
    last_link = network_links[-1]
    last_link.click()
    assert last_link.is_selected()

# Test 012: Wait for the code to appear in the “Preview” tab.
@pytest.mark.smoke
def test_012_wait_for_preview_code(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='preview']/div"))
    )
    assert driver.find_element(By.XPATH, "//div[@class='preview']/div").is_displayed()

# Test 013: Copying the code from the “Preview” tab
@pytest.mark.smoke
def test_013_copy_number(driver):
    code_element = driver.find_element(By.XPATH, "//div[@class='preview']/div")
    verification_code = code_element.text
    assert verification_code != ""

# Test 014: Finding the field for entering the SMS code and pasting the code
@pytest.mark.smoke
def test_014_enter_number(driver):
    verification_code = data.UrbanRoutesData.VERIFICATION_CODE  # Usar el código de verificación de data.py
    sms_input = driver.find_element(By.ID, "codigo_sms")
    sms_input.clear()
    sms_input.send_keys(verification_code)
    assert sms_input.get_attribute("value") == verification_code

# Prueba 015: Hacer click en el botón "Confirmar"
@pytest.mark.smoke
def test_015_select_button(driver):
    confirm_button = driver.find_element(By.XPATH, "//button[text()='Confirmar']")
    confirm_button.click()
    assert confirm_button.is_displayed()

# Test 015: Click on the “Confirm” button.
@pytest.mark.smoke
def test_016_select_arrow(driver):
    payment_arrow = driver.find_element(By.XPATH, "//img[@alt='Arrow right']")
    payment_arrow.click()
    assert payment_arrow.is_displayed()

# Test 017: Click on “Add a card”.
@pytest.mark.smoke
def test_017_add_card(driver):
    add_card = driver.find_element(By.XPATH, "//div[text()='Agregar una tarjeta']")
    add_card.click()
    assert add_card.is_displayed()

# Test 018: Enter the card number and its verification code
@pytest.mark.smoke
def test_018_enter_number(driver):
    card_number_input = driver.find_element(By.ID, "number")
    card_number_input.clear()
    card_number_input.send_keys(data.UrbanRoutesData.CARD_NUMBER)
    assert card_number_input.get_attribute("value") == data.UrbanRoutesData.CARD_NUMBER

# Test 019: Write the verification code of the card
@pytest.mark.smoke
def test_019_enter_number(driver):
    code_input = driver.find_element(By.ID, "code")
    code_input.clear()
    code_input.send_keys(data.UrbanRoutesData.CARD_CODE)
    assert code_input.get_attribute("value") == data.UrbanRoutesData.CARD_CODE

# Test 020: Click (white part) outside the main box to activate the “Link” button.
@pytest.mark.smoke
def test_020_select_overlay(driver):
    overlay = driver.find_element(By.CLASS_NAME, "overlay")
    overlay.click()
    assert overlay.is_enabled()

# Test 021: Click on the “Link” button.
@pytest.mark.smoke
def test_021_select_link(driver):
    enlace_button = driver.find_element(By.XPATH, "//button[text()='Enlace']")
    enlace_button.click()
    assert enlace_button.is_displayed()

# Test 022: Click on the close window button.
@pytest.mark.smoke
def test_022_select_button(driver):
    close_button = driver.find_element(By.CLASS_NAME, "close-button")
    close_button.click()
    assert close_button.is_displayed()

# Test 023: Add driver comment
@pytest.mark.smoke
def test_023_add_text(driver):
    comment_input = driver.find_element(By.ID, "comment")
    comment_input.clear()
    comment_input.send_keys(data.UrbanRoutesData.MESSAGE_FOR_DRIVER)
    assert comment_input.get_attribute("value") == data.UrbanRoutesData.MESSAGE_FOR_DRIVER

# Test 024: Activate the “blankets and handkerchiefs” button.
@pytest.mark.smoke
def test_024_select_button(driver):
    blankets_button = driver.find_element(By.CLASS_NAME, "slider")
    blankets_button.click()
    assert blankets_button.is_selected()

# Test 025: Add 2 ice creams
@pytest.mark.smoke
def test_025_select_button(driver):
    ice_cream_button = driver.find_element(By.CLASS_NAME, "counter-plus")
    ice_cream_button.click()
    ice_cream_button.click()
    assert "counter-plus" in driver.page_source

# Test 026: Click on the “Order a cab” button.
@pytest.mark.smoke
def test_026_select_button(driver):
    request_taxi_button_2 = driver.find_element(By.CLASS_NAME, "smart-button-main")
    request_taxi_button_2.click()
    assert request_taxi_button_2.is_displayed()

# Test 027: Wait for the “Bender” figure to appear.
@pytest.mark.smoke
def test_027_webdriverwait(driver):
    bender_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='close']"))
    )
    assert bender_image.is_displayed()

# Wait 5 seconds and close the page
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
