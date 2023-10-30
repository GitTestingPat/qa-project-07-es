from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


    # Tiempo de espera
    time.sleep(5)

    driver.quit()
