# Copy and paste the selenium script that is being generated.
# Below is the sample of generated code .

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Test Case Details ---
TEST_ID = "TC_APPLY_COUPON_001"
TEST_DESCRIPTION = "Verify successful application of a valid coupon code."
TEST_FEATURE = "Coupon Application"
TEST_SCENARIO = "User applies a valid coupon code 'SAVE15' through the UI."
EXPECTED_RESULT = "The API should return a 200 OK status and the message 'Coupon applied successfully.'."
GROUNDED_IN = "api_endpoints.json"

# URL of the local HTML file
HTML_FILE_PATH = "file:///C:/Users/irish/OneDrive/Desktop/qa_agent/assets/checkout.html"

# Coupon code to use (from available codes in HTML: SAVE15, SAVE20, DISCOUNT10, VALID10)
VALID_COUPON_CODE = "SAVE15"
EXPECTED_UI_MESSAGE = "Coupon applied successfully." # Based on Expected Result

driver = None
try:
    print("=" * 70)
    print(f"🧪 TEST CASE: {TEST_ID} - {TEST_DESCRIPTION}")
    print("=" * 70)

    print("\n✓ Initializing Edge WebDriver...")
    driver = webdriver.Edge()
    
    print(f"✓ Navigating to HTML file: {HTML_FILE_PATH}...")
    driver.get(HTML_FILE_PATH)

    wait = WebDriverWait(driver, 10)

    print(f"✓ Locating the 'Discount Code' input field (id='promo-code')...")
    promo_code_input = wait.until(
        EC.presence_of_element_located((By.ID, "promo-code"))
    )
    print(f"✓ Entering coupon code '{VALID_COUPON_CODE}'...")
    promo_code_input.send_keys(VALID_COUPON_CODE)

    print(f"✓ Locating the 'Apply' button (id='apply-promo')...")
    apply_promo_button = wait.until(
        EC.element_to_be_clickable((By.ID, "apply-promo"))
    )
    print("✓ Clicking the 'Apply' button...")
    apply_promo_button.click()

    print(f"✓ Waiting for the promo message (id='promo-message') to be visible and contain the success message...")
    promo_message_element = wait.until(
        EC.visibility_of_element_located((By.ID, "promo-message"))
    )
    
    actual_message = promo_message_element.text.strip()
    print(f"✓ Actual message displayed: '{actual_message}'")

    print(f"✓ Asserting that the message contains '{EXPECTED_UI_MESSAGE}'...")
    assert EXPECTED_UI_MESSAGE in actual_message, \
        f"Expected message '{EXPECTED_UI_MESSAGE}' not found in actual message '{actual_message}'."

    print("\n" + "=" * 70)
    print(f"✅ TEST PASSED: Coupon '{VALID_COUPON_CODE}' applied successfully and message '{EXPECTED_UI_MESSAGE}' displayed.")
    print("=" * 70)

    # Print structured test case summary
    print()
    print(f"Test_ID: {TEST_ID}")
    print(f"Feature: {TEST_FEATURE}")
    print(f"Test_Scenario: {TEST_SCENARIO}")
    print(f"Expected_Result: {EXPECTED_RESULT}")
    print(f"Grounded_In: {GROUNDED_IN}")

except Exception as e:
    print("\n" + "=" * 70)
    print(f"❌ TEST FAILED: {TEST_ID}")
    print("=" * 70)
    print(f"Error: {str(e)}")
    print("=" * 70)
    
    # Print structured test case summary on failure too
    print()
    print(f"Test_ID: {TEST_ID}")
    print(f"Feature: {TEST_FEATURE}")
    print(f"Test_Scenario: {TEST_SCENARIO}")
    print(f"Expected_Result: {EXPECTED_RESULT}")
    print(f"Grounded_In: {GROUNDED_IN}")
    
    sys.exit(1)
    
finally:
    if driver:
        print("\n✓ Closing browser...")
        driver.quit()
        print("✓ Test execution complete.\n")
