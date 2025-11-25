# Copy paste your code here and run it .

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # --- Test Case Header ---
    print("=" * 70)
    print("🧪 TEST CASE: TC001 - Verify applying a valid coupon code.")
    print("=" * 70)

    # --- Step 1: Initialize Edge WebDriver ---
    print("\n✓ Initializing Edge WebDriver...")
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10) # Initialize WebDriverWait with a 10-second timeout
    print("✓ Edge WebDriver initialized.")

    # --- Step 2: Navigate to the local HTML file ---
    print("✓ Navigating to HTML file...")
    # Use the specified local file path
    html_file_path = "file:///C:/Users/irish/OneDrive/Desktop/qa_agent/assets/checkout.html"
    driver.get(html_file_path)
    print(f"✓ Page loaded: {html_file_path}")

    # --- Step 3: Locate the 'Discount Code' input field and enter a valid code ---
    print("✓ Locating 'Discount Code' input field (ID: promo-code)...")
    promo_code_input = wait.until(EC.visibility_of_element_located((By.ID, "promo-code")))
    print("✓ 'Discount Code' input field found.")

    valid_coupon_code = "SAVE15" # A valid code from the provided HTML source hint
    print(f"✓ Entering valid coupon code: '{valid_coupon_code}'...")
    promo_code_input.send_keys(valid_coupon_code)
    print("✓ Coupon code entered.")

    # --- Step 4: Locate and click the 'Apply' button ---
    print("✓ Locating 'Apply' button (ID: apply-promo)...")
    apply_button = wait.until(EC.element_to_be_clickable((By.ID, "apply-promo")))
    print("✓ 'Apply' button found.")

    print("✓ Clicking 'Apply' button...")
    apply_button.click()
    print("✓ 'Apply' button clicked.")

    # --- Step 5: Verify the success message ---
    expected_success_message = "Coupon applied successfully."
    print(f"✓ Waiting for success message: '{expected_success_message}' to appear in 'promo-message' div (ID: promo-message)...")
    
    # Wait for the promo message element to be visible and contain the expected text
    # This also acts as an assertion that the element eventually gets the text
    wait.until(EC.text_to_be_present_in_element((By.ID, "promo-message"), expected_success_message))
    
    # Retrieve the actual message for final verification
    promo_message_element = driver.find_element(By.ID, "promo-message")
    actual_message = promo_message_element.text.strip()
    
    print(f"✓ Observed message in promo-message div: '{actual_message}'")

    # --- Step 6: Assert the expected result ---
    print("✓ Asserting expected success message...")
    assert actual_message == expected_success_message, \
        f"Assertion Failed: Expected message '{expected_success_message}', but got '{actual_message}'"
    print("✓ Assertion Passed: Coupon application success message verified.")

    # --- Test Case Passed Message ---
    print("\n" + "=" * 70)
    print("✅ TEST PASSED: TC001 - Valid coupon applied successfully.")
    print("=" * 70)

except Exception as e:
    # --- Test Case Failed Message ---
    print("\n" + "=" * 70)
    print("❌ TEST FAILED: TC001 - Verify applying a valid coupon code.")
    print("=" * 70)
    print(f"Error: {str(e)}")
    print("=" * 70)
    sys.exit(1) # Exit with a non-zero status code to indicate failure

finally:
    # --- Clean up: Close the browser ---
    if 'driver' in locals() and driver:
        print("\n✓ Closing browser...")
        driver.quit()
        print("✓ Test execution complete.\n")