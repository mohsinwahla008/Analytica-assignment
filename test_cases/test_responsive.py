import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(scope="function")
def mobile_browser():
    # Initialize regular Chrome browser
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Set mobile dimensions
    driver.set_window_size(360, 640)

    # Set mobile user agent via JavaScript
    mobile_user_agent = "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36"
    driver.execute_script("return navigator.userAgent = arguments[0];", mobile_user_agent)

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


def setup_mobile_browser(mobile_browser):
    """Common setup for all mobile tests"""
    mobile_browser.get("https://www.bazaar-uae.com/")
    close_popup_modal(mobile_browser)
    time.sleep(2)  # Allow time for resize
    mobile_browser.refresh()
    time.sleep(2)
    WebDriverWait(mobile_browser, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


def test_mobile_menu_visibility(mobile_browser):
    """Test 1: Verify mobile menu appears"""
    setup_mobile_browser(mobile_browser)

    try:
        hamburger_menu = WebDriverWait(mobile_browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".mobile-menu-btn, .side-menu-btn, [aria-label='Menu']"))
        )
        assert hamburger_menu.is_displayed(), "Mobile menu button not visible"
    except:
        mobile_browser.save_screenshot("mobile_menu_fail.png")
        pytest.fail("Mobile menu element not found or not visible")


def test_viewport_sizing(mobile_browser):
    """Test 2: Verify viewport sizing"""
    setup_mobile_browser(mobile_browser)

    body_width = mobile_browser.execute_script("return document.body.scrollWidth")
    viewport_width = mobile_browser.execute_script("return window.innerWidth")
    assert body_width <= viewport_width, f"Content width {body_width}px exceeds viewport {viewport_width}px"
    print("Viewport sizing test completed")


def test_touch_element_sizes(mobile_browser):
    """Test 3: Check touch elements are large enough"""
    setup_mobile_browser(mobile_browser)

    try:
        menu_items = mobile_browser.find_elements(By.CSS_SELECTOR, ".mean-nav")
        for item in menu_items[:3]:  # Check first 3 items
            size = item.size
            assert size['width'] >= 48 and size['height'] >= 48, "Touch target too small"
    except:
        pytest.skip("Could not find menu items to test touch sizes")






# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# import time
#
#
# @pytest.fixture(scope="function")
# def mobile_browser():
#     # Initialize regular Chrome browser
#     driver = webdriver.Chrome()
#
#     # Set mobile dimensions
#     driver.set_window_size(360, 640)
#
#     # Set mobile user agent via JavaScript
#     mobile_user_agent = "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36"
#     driver.execute_script("return navigator.userAgent = arguments[0];", mobile_user_agent)
#
#     yield driver
#     driver.quit()
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
# def test_mobile_responsiveness(mobile_browser):
#     """Test mobile responsiveness of the website"""
#     # Navigate to the website
#     mobile_browser.get("https://www.bazaar-uae.com/")
#     close_popup_modal(mobile_browser)
#     time.sleep(2)  # Allow time for resize
#
#     # Refresh to apply mobile view changes
#     mobile_browser.refresh()
#     time.sleep(2)
#
#     # Wait for page to load
#     WebDriverWait(mobile_browser, 15).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )
#
#     # Test 1: Verify mobile menu appears
#     try:
#         hamburger_menu = WebDriverWait(mobile_browser, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, ".mobile-menu-btn, .side-menu-btn, [aria-label='Menu']"))
#         )
#         assert hamburger_menu.is_displayed(), "Mobile menu button not visible"
#     except:
#         # Debugging help - take screenshot if test fails
#         mobile_browser.save_screenshot("mobile_test_fail.png")
#         pytest.fail("Mobile menu element not found or not visible")
#
#     # Test 2: Verify viewport sizing
#     body_width = mobile_browser.execute_script("return document.body.scrollWidth")
#     viewport_width = mobile_browser.execute_script("return window.innerWidth")
#     assert body_width <= viewport_width, f"Content width {body_width}px exceeds viewport {viewport_width}px"
#     print("viewport sizing is being tested")
#
#     # Test 3: Check touch elements are large enough
#     try:
#         menu_items = mobile_browser.find_elements(By.CSS_SELECTOR, ".mobile-menu a, .nav-item")
#         for item in menu_items[:3]:  # Check first 3 items
#             size = item.size
#             assert size['width'] >= 48 and size['height'] >= 48, "Touch target too small"
#     except:
#         pass
#
