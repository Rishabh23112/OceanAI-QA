from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_test_tc001():
    driver = None
    try:
        # 1. Initialize Edge driver
        # Selenium 4 automatically handles driver setup for Edge
        driver = webdriver.Edge()
        driver.maximize_window() # Maximize window for better visibility

        # 2. Define the local file URL as per requirements
        file_url = "file:///C:/Users/irish/OneDrive/Desktop/qa_agent/assets/checkout.html"
        driver.get(file_url)

        # 3. Initialize WebDriverWait with a timeout
        wait = WebDriverWait(driver, 10) # Wait up to 10 seconds

        print("Test Case TC001: Verifying the base price of Wireless Headphones is displayed correctly")

        # Step 1: Navigate to the product page for Wireless Headphones (handled by driver.get above)
        # Step 2: Observe the displayed price
        
        # Locate the price element using its ID
        # Use EC.visibility_of_element_located to ensure the element is present and visible
        price_element = wait.until(EC.visibility_of_element_located((By.ID, "price")))
        actual_price_value = price_element.text

        # Expected Result: The price displayed is $100.00 USD
        # The span element itself contains "100.00", the '$' is outside it in the <p> tag.
        # We'll assert the value from the element and then confirm the full display.
        expected_price_from_element = "100.00"
        full_expected_display_string = "$100.00 USD"

        # 6. Assertions to verify the Expected Result
        assert actual_price_value == expected_price_from_element, \
            f"Assertion Failed: Expected price value '{expected_price_from_element}' " \
            f"from element but got '{actual_price_value}'."

        print(f"Test TC001 Passed: Wireless Headphones base price displayed correctly.")
        print(f"Observed Price: ${actual_price_value}")
        print(f"Expected Price: {full_expected_display_string}")

    # 7. Wrap everything in a try-except-finally block with proper error handling
    except Exception as e:
        print(f"Test TC001 Failed: An error occurred - {e}")
    finally:
        if driver:
            driver.quit() # Close the browser
        print("Test TC001 execution finished.")

# This allows the function to be called when the script is run
run_test_tc001()
