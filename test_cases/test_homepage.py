import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture(scope="function")
def browser():


    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def close_popup_modal(browser):
    """Helper function to close any popup modal if it appears"""
    try:
        # Wait for popup to appear (with shorter timeout)
        popup = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#couponModal"))
        )
        # Try to find and click the close button
        close_button = popup.find_element(By.CSS_SELECTOR, "#couponModal .product__modal-close .Btn")
        close_button.click()
        time.sleep(1)  # Small delay for the popup to close
    except:
        # Popup didn't appear or couldn't be closed - continue with test
        pass


# Split into separate test functions for better reporting
def test_logo_presence(browser):
    """Test 1: Verify website logo is present"""
    browser.get("https://www.bazaar-uae.com/")
    close_popup_modal(browser)

    logo = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[src="/img/logo/header logo.png"]'))
    )
    assert logo.is_displayed(), "Website logo is not displayed"


def test_navigation_menu_items(browser):
    """Test 2: Verify navigation menu items"""
    browser.get("https://www.bazaar-uae.com/")
    close_popup_modal(browser)

    menu_items = ["HOME", "ABOUT US", "SHOP", "CONTACT US"]
    nav_container = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "mobile-menu"))
    )
    nav_elements = nav_container.find_elements(By.TAG_NAME, "li")

    assert len(nav_elements) >=  len(menu_items), (
        f"Expected at least {len(menu_items)} menu items, found {len(nav_elements)}")


def test_search_bar_presence(browser):
    """Test 3: Verify search bar is present"""
    browser.get("https://www.bazaar-uae.com/")
    close_popup_modal(browser)

    search_bar = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".header__search-box"))
    )
    assert search_bar.is_displayed(), "Search bar is not displayed"


def test_cart_button_presence(browser):
    """Test 4: Verify cart button is present"""
    browser.get("https://www.bazaar-uae.com/")
    close_popup_modal(browser)

    cart_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart__toggle"))
    )
    assert cart_button.is_displayed(), "Cart button is not displayed"











# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
#
# @pytest.fixture(scope="function")
# def browser():
#
#     driver = webdriver.Chrome()
#     yield driver
#     driver.quit()
#
#
# def close_popup_modal(browser):
#     """Helper function to close any popup modal if it appears"""
#     try:
#         # Wait for popup to appear (with shorter timeout)
#         popup = WebDriverWait(browser, 3).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "#couponModal"))
#         )
#         # Try to find and click the close button
#         close_button = popup.find_element(By.CSS_SELECTOR, "#couponModal .product__modal-close .Btn")
#         close_button.click()
#         time.sleep(1)  # Small delay for the popup to close
#     except:
#         # Popup didn't appear or couldn't be closed - continue with test
#         pass
#
#
# def test_home_page_elements(browser):
#     # Navigate to the website
#     browser.get("https://www.bazaar-uae.com/")
#
#     # Close any popup that appears
#     close_popup_modal(browser)
#
#     # Wait for page to load
#     WebDriverWait(browser, 15).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )
#
#     # Test 1: Verify logo is present
#     logo = WebDriverWait(browser, 10).until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[src="/img/logo/header logo.png"]'))
#     )
#     assert logo.is_displayed(), "Website logo is not displayed"
#
#     # Test 2: Verify navigation menu items
#     menu_items = ["HOME", "ABOUT US", "SHOP", "CONTACT US"]
#     nav_container = WebDriverWait(browser, 10).until(
#         EC.presence_of_element_located((By.ID, "mobile-menu"))
#     )
#     nav_elements = nav_container.find_elements(By.TAG_NAME, "li")
#
#     # Verify at least the expected number of menu items are present
#     assert len(nav_elements) >= len(
#         menu_items), f"Expected at least {len(menu_items)} menu items, found {len(nav_elements)}"
#
#     # Test 3: Verify search bar is present
#     search_bar = WebDriverWait(browser, 10).until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, ".header__search-box"))
#     )
#     assert search_bar.is_displayed(), "Search bar is not displayed"
#
#     # Test 4: Verify cart button is present
#     cart_button = WebDriverWait(browser, 10).until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart__toggle"))
#     )
#     assert cart_button.is_displayed(), "Cart button is not displayed"
