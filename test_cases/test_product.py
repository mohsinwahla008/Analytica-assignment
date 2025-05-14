import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
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
        print("Closed popup modal")
    except:
        # Popup didn't appear or couldn't be closed - continue with test
        pass


def test_product_details(browser):
    """Test complete product page workflow"""
    try:
        # 1. Navigate to shop page
        print("Navigating to main page...")
        browser.get("https://www.bazaar-uae.com")
        close_popup_modal(browser)  # Close modal on main page

        shop_button = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "header li:nth-child(3) a:nth-child(1)"))
        )
        shop_button.click()
        time.sleep(5)
        close_popup_modal(browser)  # Close modal after navigation if it appears

        # 2. Find and click first product
        print("Locating first product...")
        product = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/product-details/2414008d-6546-49e0-9a65-308d247f88ed']"))
        )
        browser.execute_script("""
            arguments[0].scrollIntoView({behavior: 'smooth', block: 'nearest'});
        """, product)
        time.sleep(1)  # Smooth scroll
        product.click()
        print("Clicked on product")
        time.sleep(10)
          # Close modal on product details page

        # 3. Wait for product details page
        print("Waiting for product details...")
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product__details, .product-detail, .product-container"))
        )
        close_popup_modal(browser)
        # 4. Test product title
        print("Checking product title...")
        title = WebDriverWait(browser, 15).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".product__details-title, .product-title, h1.product-name"))
        )
        assert title.is_displayed() and title.text.strip(), "Product title missing or empty"
        print(f"Product: {title.text}")

        # 5. Test product price
        print("Checking product price...")
        price = WebDriverWait(browser, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#priceVal, .product-price, .price, [itemprop='price']"))
        )
        assert price.is_displayed() and ("AED" in price.text or "$" in price.text), "Invalid price format"
        print(f"Price: {price.text}")

        # 6. Test add to cart button
        print("Checking add to cart button...")
        add_to_cart = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".pro-cart-btn, .add-to-cart, button.add-cart"))
        )
        add_to_cart.click()
        print("Clicked add to cart")

        # 7. Verify success notification
        try:
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message, .added-to-cart"))
            )
            print("Add to cart successful")
        except TimeoutException:
            print("No success notification, but continuing")

        # 8. Verify product image
        print("Checking product images...")
        images = WebDriverWait(browser, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "img.product-image, .product-gallery img, img[alt*='product']"))
        )
        assert len(images) >= 1, "No product images found"
        print(f"Found {len(images)} product images")

    except Exception as e:
        browser.save_screenshot("test_failure.png")
        print(f"Test failed at step: {e}")
        raise





# import time
# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# @pytest.fixture(scope="module")
# def browser():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
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
# def test_product_details(browser):
#     """Test complete product page workflow"""
#     try:
#         # 1. Navigate to shop page
#         print("Navigating to main page...")
#         browser.get("https://www.bazaar-uae.com")
#         close_popup_modal(browser)
#
#         shop_button = WebDriverWait(browser, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "header li:nth-child(3) a:nth-child(1)"))
#
#         )
#         shop_button.click()
#         time.sleep(5)
#
#
#         # 2. Find and click first product
#         print("Locating first product...")
#         product = WebDriverWait(browser, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/product-details/2414008d-6546-49e0-9a65-308d247f88ed']"))
#         )
#         browser.execute_script("""
#             arguments[0].scrollIntoView({behavior: 'smooth', block: 'nearest'});
#         """, product)
#         time.sleep(1)  # Smooth scroll
#         product.click()
#         print("Clicked on product")
#         time.sleep(3)
#
#
#         # 3. Wait for product details page
#         print("Waiting for product details...")
#         WebDriverWait(browser, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".product__details, .product-detail, .product-container"))
#         )
#
#         # 4. Test product title
#         print("Checking product title...")
#         title = WebDriverWait(browser, 15).until(
#             EC.visibility_of_element_located(
#                 (By.CSS_SELECTOR, ".product__details-title, .product-title, h1.product-name"))
#         )
#         assert title.is_displayed() and title.text.strip(), "Product title missing or empty"
#         print(f"Product: {title.text}")
#
#         # 5. Test product price
#         print("Checking product price...")
#         price = WebDriverWait(browser, 15).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "#priceVal, .product-price, .price, [itemprop='price']"))
#         )
#         assert price.is_displayed() and ("AED" in price.text or "$" in price.text), "Invalid price format"
#         print(f"Price: {price.text}")
#
#         # 6. Test add to cart button
#         print("Checking add to cart button...")
#         add_to_cart = WebDriverWait(browser, 15).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".pro-cart-btn, .add-to-cart, button.add-cart"))
#         )
#         add_to_cart.click()
#         print("Clicked add to cart")
#
#         # 7. Verify success notification
#         try:
#             WebDriverWait(browser, 10).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message, .added-to-cart"))
#             )
#             print("Add to cart successful")
#         except TimeoutException:
#             print("No success notification, but continuing")
#
#         # 8. Verify product image
#         print("Checking product images...")
#         images = WebDriverWait(browser, 15).until(
#             EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, "img.product-image, .product-gallery img, img[alt*='product']"))
#         )
#         assert len(images) >= 1, "No product images found"
#         print(f"Found {len(images)} product images")
#
#     except Exception as e:
#         browser.save_screenshot("test_failure.png")
#         print(f"Test failed at step: {e}")
#         raise