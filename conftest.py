import pytest
from selenium import webdriver


@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome() as driver:
        yield driver
