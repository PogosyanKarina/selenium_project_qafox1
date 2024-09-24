from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.mark.smoke
@pytest.fixture(scope="module")
def driver():
    """
      Creates an instance of the Chrome web driver with configured options.

      Uses headless mode to run the browser without a graphical interface.
      Sets the maximum window size and implicit wait time for elements.

      Returns:
          webdriver.Chrome: An initialized instance of the web driver.
      """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--window-size = 1920x1018")
    # chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.smoke
@pytest.mark.regression
@pytest.fixture(scope='function')
def login(driver):
    driver.get('https://tutorialsninja.com/demo/index.php?route=account/login')

    # Fill in the login form
    driver.find_element(By.NAME,'email').send_keys('pogosyan@yandex.ru')  #
    driver.find_element(By.NAME, 'password').send_keys('karina1234$')

    # Click the login button
    driver.find_element(By.CSS_SELECTOR, 'input.btn.btn-primary').click()

    # Wait for the success message or account dashboard to verify login
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2'))
    )

    assert "My Account" in driver.page_source, "Login failed."
