import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import allure


@allure.feature('Menu Navigation')
@allure.suite('UI Tests')
@allure.title('Test Menu Item Navigation')
@allure.description(
    'Verifies that each menu item on the homepage navigates to the correct '
    'page and displays the correct heading.')
@allure.severity(allure.severity_level.CRITICAL)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_menu_item(driver):

    with allure.step("Opening the homepage"):
        driver.get("https://tutorialsninja.com/demo/")
    expected_menu_items = ["Desktops", "Laptops & Notebooks", "Components", "Tablets", "Software",
                           "Phones & PDAs", "Cameras", "MP3 Players"]

    with allure.step(f"Clicking on menu item: {expected_menu_items[0]}"):
        menu_item1 = driver.find_element(By.LINK_TEXT, expected_menu_items[0])
        menu_item1.click()

    with allure.step(f"Clicking on menu item: {expected_menu_items[1]}"):
        menu_item2 = driver.find_element(By.LINK_TEXT, expected_menu_items[1])
        menu_item2.click()

    with allure.step(f"Clicking on menu item: {expected_menu_items[2]}"):
        menu_item3 = driver.find_element(By.LINK_TEXT, expected_menu_items[2])
        menu_item3.click()

    with allure.step(f"Clicking on menu item: {expected_menu_items[3]}"):
        menu_item4 = driver.find_element(By.LINK_TEXT, expected_menu_items[3])
        menu_item4.click()

    with allure.step(f"Verifying the page heading for {expected_menu_items[3]}"):
        assert driver.find_element(By.TAG_NAME, 'h2').text == expected_menu_items[3]

    with allure.step(f"Clicking on menu item: {expected_menu_items[4]}"):
        menu_item5 = driver.find_element(By.LINK_TEXT, expected_menu_items[4])
        menu_item5.click()
    with allure.step(f"Verifying the page heading for {expected_menu_items[4]}"):
        assert driver.find_element(By.TAG_NAME, 'h2').text == expected_menu_items[4]

    with allure.step(f"Clicking on menu item: {expected_menu_items[5]}"):
        menu_item6 = driver.find_element(By.LINK_TEXT, expected_menu_items[5])
        menu_item6.click()
    assert driver.find_element(By.TAG_NAME, 'h2').text == expected_menu_items[5]

    menu_item7 = driver.find_element(By.LINK_TEXT, expected_menu_items[6])
    menu_item7.click()
    assert driver.find_element(By.TAG_NAME, 'h2').text == expected_menu_items[6]

    menu_item8 = driver.find_element(By.LINK_TEXT, expected_menu_items[7])
    menu_item8.click()


@pytest.mark.smoke
@pytest.mark.parametrize("menu_locator, submenu_locator, result_text", [
    (
            (By.PARTIAL_LINK_TEXT, 'Desktops'),
            (By.XPATH, '//*[@id="menu"]/div[2]/ul/li[1]/div/div/ul/li[1]/a'),
            'PC'
    ),
    (
            (By.PARTIAL_LINK_TEXT, 'Desktops'),
            (By.XPATH, '//*[@id="menu"]/div[2]/ul/li[1]/div/div/ul/li[2]/a'),
            "Mac"
    ),
    (
            (By.PARTIAL_LINK_TEXT, 'Laptops'),
            (By.XPATH, '//*[@id="menu"]/div[2]/ul/li[2]/div/div/ul/li[1]/a'),
            "Macs"
    ),
    (
            (By.PARTIAL_LINK_TEXT, 'Laptops'),
            (By.XPATH, '//*[@id="menu"]/div[2]/ul/li[2]/div/div/ul/li[2]/a'),
            "Windows"
    ),
    (
            (By.PARTIAL_LINK_TEXT, 'Components'),
            (By.XPATH, '//*[@id="menu"]/div[2]/ul/li[3]/div/div/ul/li[1]/a'),
            "Mice and Trackballs"
    ),
    (
            (By.PARTIAL_LINK_TEXT, 'Components'),
            (By.XPATH, '//*[@id="menu"]/div[2]/ul/li[3]/div/div/ul/li[2]/a'),
            "Monitors"
    )
])
@pytest.mark.regression
def test_nested_menu(driver, menu_locator, submenu_locator, result_text):
    driver.get('https://tutorialsninja.com/demo/')

    with allure.step(f"Hovering over menu: {menu_locator[1]} and clicking submenu: {submenu_locator[1]}"):
        menu = driver.find_element(*menu_locator)
        submenu = driver.find_element(*submenu_locator)
        ActionChains(driver).move_to_element(menu).click(submenu).perform()

    with allure.step(f"Verifying the result text: {result_text}"):
        assert driver.find_element(By.TAG_NAME, "h2").text == result_text


@pytest.mark.regression
def test_search_product(driver):
    driver.get('https://tutorialsninja.com/demo/')
    with allure.step("Searching for product 'MacBook'"):
        search = driver.find_element(By.NAME, 'search')
        search.send_keys("MacBook")
        button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-lg')
        button.click()

    with allure.step("Verifying search results contain 'MacBook'"):
        products = driver.find_elements(By.TAG_NAME, 'h4')
        new_list = [elem.text for elem in products if 'MacBook' in elem.text]
        assert len(products) == len(new_list)


@pytest.mark.regression
def test_add_to_cart(driver):
    driver.get('https://tutorialsninja.com/demo/')

    with allure.step("Adding product to cart"):
        product = driver.find_element(By.XPATH,
                                      '//*[@id="content"]/div[2]/div[1]/div/div[3]/button[1]')
        product.click()

    with allure.step("Verifying success message"):
        success_message = WebDriverWait(driver, timeout=20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-success"))
        )
        assert "Success: You have added" in success_message.text

    with allure.step("Checking cart contents"):
        WebDriverWait(driver, timeout=20).until(
            EC.text_to_be_present_in_element((By.ID, 'cart-total'), "1 item(s)")
        )

        cart_button = WebDriverWait(driver, timeout=20).until(
            EC.element_to_be_clickable((By.ID, "cart"))
        )
        cart_button.click()

        cart_contents = WebDriverWait(driver, timeout=20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.dropdown-menu.pull-right"))
        )

        # Scroll into view to ensure visibility
        driver.execute_script("arguments[0].scrollIntoView(true);", cart_contents)

        cart_text = cart_contents.text
        print("Cart contents text:", cart_text)  # Print out the text for debugging

        assert "MacBook" in cart_text, f"Expected 'MacBook' in cart but got '{cart_text}'"


@pytest.mark.regression
def test_slider_functionality(driver):
    driver.get('https://tutorialsninja.com/demo/')
    with allure.step("Verifying slider is visible"):
        slider = driver.find_element(By.CLASS_NAME, 'swiper-container')
        assert slider.is_displayed(), 'Slider is not visible on the page.'

    first_slide = driver.find_element(By.CSS_SELECTOR, ".swiper-slide-active img")
    first_slide_src = first_slide.get_attribute("src")

    next_arrow = driver.find_element(By.CLASS_NAME, "swiper-button-next")

    with allure.step("Clicking next arrow on slider"):
        ActionChains(driver).move_to_element(slider).click(next_arrow).perform()

    WebDriverWait(driver, 20).until_not(
        EC.element_to_be_clickable(first_slide)
    )

    new_slide = driver.find_element(By.CSS_SELECTOR, ".swiper-slide-active img")
    new_slide_src = new_slide.get_attribute('src')

    with allure.step("Verifying the slider moved to the next image"):
        assert first_slide_src != new_slide_src, "Slider did not move to the next image."

    prev_arrow = driver.find_element(By.CLASS_NAME, "swiper-button-prev")
    with allure.step("Clicking previous arrow on slider"):
        prev_arrow.click()

    WebDriverWait(driver, 20).until_not(
        EC.element_to_be_clickable(new_slide)
    )

    reversed_slide_src = driver.find_element(By.CSS_SELECTOR,
                                             ".swiper-slide-active img").get_attribute("src")

    with allure.step("Verifying the slider returned to the first image"):
        assert reversed_slide_src == first_slide_src, "Slider did not return to the first image"


@pytest.mark.regression
def test_add_to_wishlist(driver, login):
    driver.get('https://tutorialsninja.com/demo/')

    with allure.step("Adding product to wishlist"):
        for attempt in range(3):
            try:
                wishlist_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '//*[@id="content"]/div[2]/div[1]/div/div[3]/button[2]'))
                )
                wishlist_button.click()
                break
            except StaleElementReferenceException:
                print("1, Element is stale, retrying...")

    with allure.step("Verifying success message after adding to wishlist"):
        success_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-success"))
        )
        print("Success message:", success_message.text)


@pytest.mark.regression
@pytest.mark.parametrize('button, header, expected_text', [
    (
            (By.XPATH, '/html/body/footer/div/div/div[1]/ul/li[1]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            'About Us'
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[1]/ul/li[2]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            'Delivery Information'
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[1]/ul/li[3]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Privacy Policy"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[1]/ul/li[4]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Terms & Conditions"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[2]/ul/li[1]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Contact Us"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[2]/ul/li[2]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Product Returns"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[2]/ul/li[3]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Site Map"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[3]/ul/li[1]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Find Your Favorite Brand"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[3]/ul/li[2]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Purchase a Gift Certificate"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[3]/ul/li[3]/a'),
            (By.XPATH, '//*[@id="content"]/h2[3]'),
            "My Affiliate Account"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[3]/ul/li[4]/a'),
            (By.XPATH, '//*[@id="content"]/h2'),
            "Special Offers"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[4]/ul/li[1]/a'),
            (By.XPATH, '//*[@id="content"]/h2[1]'),
            "My Account"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[4]/ul/li[2]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Order History"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[4]/ul/li[3]/a'),
            (By.XPATH, '//*[@id="content"]/h2'),
            "My Wish List"
    ),
    (
            (By.XPATH, '/html/body/footer/div/div/div[4]/ul/li[4]/a'),
            (By.XPATH, '//*[@id="content"]/h1'),
            "Newsletter Subscription"
    ),
])
@pytest.mark.regression
def test_footer(driver, button, header, expected_text):
    driver.get("https://tutorialsninja.com/demo/")

    with allure.step(f"Clicking footer button: {button[1]}"):
        footer_button = driver.find_element(*button)
        footer_button.click()

    with allure.step(f"Verifying header for expected text: {expected_text}"):
        footer_header_text = driver.find_element(*header).text
        assert footer_header_text == expected_text, (f"Expected '{expected_text}' "
                                                     f"but got '{footer_header_text}'")
