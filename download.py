from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time

# Configuration for ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Set up download directory
current_dir = os.getcwd()
prefs = {
    "download.default_directory": current_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Path to ChromeDriver (replace with your own path)
service = Service('/usr/local/bin/chromedriver')  # Replace with the path to your ChromeDriver

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.screener.in/")

    # Navigate to login
    login_button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "account", " " ))]'))
    )
    login_button.click()

    # Enter login credentials
    email_input = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="id_username"]'))
    )
    password_input = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="id_password"]'))
    )
    email_input.send_keys("mahekh@gmail.com")
    password_input.send_keys("mahekh2002")

    # Click the login button
    second_login_button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-user", " " ))]'))
    )
    second_login_button.click()

    # Navigate to the desired page
    driver.get("https://www.screener.in/company/RELIANCE/consolidated/")

    # Wait for the download button to be clickable and click it
    export_button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-download", " " ))]'))
    )
    export_button.click()

    # Wait for the download to complete by checking for files in the download directory
    time.sleep(10)  # Adjust this delay if necessary
    print("Files in download directory after wait:", os.listdir(current_dir))

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()   
