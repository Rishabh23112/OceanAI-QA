import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # Test Header
    test_id = "APICOUPON_001"
    test_description = "Verify successful application of a valid coupon code."
    print("=" * 70)
    print(f"🧪 TEST CASE: {test_id} - {test_description}")
    print("=" * 70)

    # 1. Initializing Edge WebDriver
    print("\n✓ Initializing Edge WebDriver...")
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10) # Initialize WebDriverWait with a 10-second timeout

    # 2. Navigating to the local HTML file
    html_file_path = "file:///C:/Users/irish/OneDrive/Desktop/qa_agent/assets/checkout.html"
    print(f"✓ Navigating to HTML file: {html_file_path}")
    driver.get(html_file_path)

    # Define the valid coupon code and the expected success message
    # The HTML provides "Available codes: SAVE15, SAVE20, DISCOUNT10, VALID10"
    valid_coupon_code = "SAVE15"
    # The expected result specifies "Coupon applied successfully." message
    expected_success_message = "Coupon applied successfully."

    # 3. Locating and interacting with the promo code input field
    print(f"✓ Locating 'Discount Code' input field (ID: promo-code)...")
    promo_code_input = wait.until(EC.presence_of_element_located((By.ID, "promo-code")))
    print(f"✓ Entering valid coupon code '{valid_coupon_code}'...")
    promo_code_input.send_keys(valid_coupon_code)

    # 4. Locating and clicking the 'Apply' button
    print(f"✓ Locating 'Apply' button (ID: apply-promo)...")
    apply_promo_button = wait.until(EC.element_to_be_clickable((By.ID, "apply-promo")))
    print(f"✓ Clicking 'Apply' button...")
    apply_promo_button.click()

    # 5. Verifying the success message displayed on the page
    # The success message is expected to appear in the div with ID 'promo-message'.
    print(f"✓ Waiting for success message '{expected_success_message}' to appear in promo-message (ID: promo-message)...")
    wait.until(EC.text_to_be_present_in_element((By.ID, "promo-message"), expected_success_message))

    # Retrieve the actual message from the element
    actual_message_element = driver.find_element(By.ID, "promo-message")
    actual_message = actual_message_element.text.strip()
    print(f"✓ Actual message displayed: '{actual_message}'")

    # 6. Asserting the expected result
    assert actual_message == expected_success_message, \
        f"Assertion failed: Expected message '{expected_success_message}', but got '{actual_message}'."
    print("✓ Assertion passed: Coupon application success message verified.")

    # Test Passed Output
    print("\n" + "=" * 70)
    print(f"✅ TEST PASSED: Coupon '{valid_coupon_code}' was applied successfully.")
    print("=" * 70)

except Exception as e:
    # Test Failed Output
    print("\n" + "=" * 70)
    print(f"❌ TEST FAILED: {test_id} - {test_description}")
    print("=" * 70)
    print(f"Error: {str(e)}")
    print("=" * 70)
    sys.exit(1) # Exit with a non-zero status code to indicate failure

finally:
    # Ensure the browser is closed even if the test fails
    if 'driver' in locals() and driver: # Check if 'driver' variable exists and is not None
        print("\n✓ Closing browser...")
        driver.quit()
        print("✓ Test execution complete.\n")