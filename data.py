import os
from dotenv import load_dotenv

load_dotenv()

# URL base - viene del archivo .env
BASE_URL = os.getenv('BASE_URL', 'https://qa.urban-routes.com')

class UrbanRoutesData:
    ADDRESS_FROM = "East 2nd Street, 601"
    TO_ADDRESS = "1300 1st St"
    REQUEST_TAXI = "Pedir un taxi"
    SELECT_CATEGORY = "Comfort"
    PHONE_NUMBER = "+12312312312"
    CARD_NUMBER = "1234 0000 4321 1234"
    CARD_CODE = "123"
    DRIVER_MESSAGE = "Por favor, llámame cuando llegues."