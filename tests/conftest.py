import os
import sys
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep

# Fix pytest 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='session', autouse=True)
def base_url(pytestconfig):
    return pytestconfig.getoption('base_url')

#Fixture for Firefox
@pytest.fixture(scope="class")
def ff_driver_init(request):
    options = webdriver.firefox.options.Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    ff_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options, service_log_path='tests/geckodriver.log')
    request.cls.drivers.append(ff_driver)
    yield
    ff_driver.close()

#Fixture for Chrome
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    request.cls.drivers.append(chrome_driver)
    yield
    chrome_driver.close()

@pytest.mark.usefixtures("ff_driver_init")
#@pytest.mark.usefixtures("chrome_driver_init")
class MultipleBrowserTest:
    drivers = []
    pass
