import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # Test case details for structured output
    TEST_ID = "TC001"
    TEST_DESCRIPTION = "Verify successful application of a valid coupon code."
    FEATURE = "Coupon Application"
    TEST_SCENARIO = "Apply a valid coupon code via UI and verify success message."
    # The Expected_Result is kept exactly as specified in the problem description,
    # though the Selenium script verifies its UI manifestation.
    EXPECTED_RESULT = "API returns 200 OK with 'Coupon applied successfully.'"
    GROUNDED_IN = "api_endpoints.json"

    print("=" * 70)
    print(f"🧪 TEST CASE: {TEST_ID} - {TEST_DESCRIPTION}")
    print("=" * 70)

    print("\n✓ Initializing Edge WebDriver...")
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10) # Initialize WebDriverWait with a 10-second timeout

    # As per requirement 5, assume the HTML file is local.
    HTML_FILE_PATH = "file:///C:/Users/irish/OneDrive/Desktop/qa_agent/assets/checkout.html"
    print(f"✓ Navigating to HTML file: {HTML_FILE_PATH}")
    driver.get(HTML_FILE_PATH)

    # Coupon code to use (from the HTML page's available codes)
    VALID_COUPON_CODE = "VALID10"
    # The message expected to be displayed in the UI upon successful application
    EXPECTED_UI_FEEDBACK_MESSAGE = "Coupon applied successfully."

    # Locate the Discount Code input field
    print(f"✓ Locating Discount Code input field (ID: 'promo-code')...")
    promo_code_input = wait.until(EC.presence_of_element_located((By.ID, "promo-code")))

    # Enter the valid coupon code into the input field
    print(f"✓ Entering coupon code '{VALID_COUPON_CODE}' into the input field...")
    promo_code_input.send_keys(VALID_COUPON_CODE)

    # Locate and click the Apply button
    print(f"✓ Locating 'Apply' button (ID: 'apply-promo')...")
    apply_promo_button = wait.until(EC.element_to_be_clickable((By.ID, "apply-promo")))
    print("✓ Clicking 'Apply' button...")
    apply_promo_button.click()

    # Wait for the feedback message to appear in the promo-message div
    print(f"✓ Waiting for feedback message to appear in 'promo-message' div...")
    promo_message_div = wait.until(EC.visibility_of_element_located((By.ID, "promo-message")))

    # Get the actual message and strip whitespace for robust comparison
    actual_message = promo_message_div.text.strip()

    # Assert that the expected success message is contained within the actual message
    print(f"✓ Verifying message: '{EXPECTED_UI_FEEDBACK_MESSAGE}'...")
    if EXPECTED_UI_FEEDBACK_MESSAGE in actual_message:
        print("\n" + "=" * 70)
        print(f"✅ TEST PASSED: Coupon '{VALID_COUPON_CODE}' applied successfully. Message: '{actual_message}'")
        print("=" * 70)
    else:
        # If the expected message is not found, raise an assertion error
        raise AssertionError(f"Expected success message '{EXPECTED_UI_FEEDBACK_MESSAGE}' not found in actual message: '{actual_message}'")

    # Print structured test case summary upon success
    print()
    print(f"Test_ID: {TEST_ID}")
    print(f"Feature: {FEATURE}")
    print(f"Test_Scenario: {TEST_SCENARIO}")
    print(f"Expected_Result: {EXPECTED_RESULT}")
    print(f"Grounded_In: {GROUNDED_IN}")

except Exception as e:
    print("\n" + "=" * 70)
    print(f"❌ TEST FAILED: {TEST_ID} - {TEST_DESCRIPTION}")
    print("=" * 70)
    print(f"Error: {str(e)}")
    print("=" * 70)

    # Print structured test case summary upon failure
    print()
    print(f"Test_ID: {TEST_ID}")
    print(f"Feature: {FEATURE}")
    print(f"Test_Scenario: {TEST_SCENARIO}")
    print(f"Expected_Result: {EXPECTED_RESULT}")
    print(f"Grounded_In: {GROUNDED_IN}")

    sys.exit(1) # Exit with a non-zero status code to indicate failure

finally:
    # Ensure the browser is closed even if an error occurs
    if 'driver' in locals() and driver:
        print("\n✓ Closing browser...")
        driver.quit()
        print("✓ Test execution complete.\n")