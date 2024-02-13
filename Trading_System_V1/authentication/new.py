from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Initialize the WebDriver session
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Paytm Money login page
driver.get("https://login.paytmmoney.com/")

# Check if the login form is present
try:
    # Wait for the email input to be clickable, then click on it
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
    )
    email_input.click()  # Click on the email field to activate it

    # Wait a moment for any potential JavaScript after clicking
    WebDriverWait(driver, 2).until(lambda d: email_input == d.switch_to.active_element)

    # Now send the keys
    email_input.send_keys("your_email@example.com")

    # Wait for the password input to be clickable, then click on it
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_input.click()  # Click on the password field to activate it

    # Wait a moment for any potential JavaScript after clicking
    WebDriverWait(driver, 2).until(lambda d: password_input == d.switch_to.active_element)

    # Now send the keys
    password_input.send_keys("your_password")

    # Find and click the login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()

    # Proceed with any further actions after login, e.g., handling 2FA

except Exception as e:
    print(f"An error occurred: {e}")