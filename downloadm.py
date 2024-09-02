from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import os
# ============================================================ #
# Set up Chrome options
current_dir = os.getcwd()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
# Configure download preferences
prefs = {
   "download.default_directory": current_dir,
   "download.prompt_for_download": False,
   "download.directory_upgrade": True,
   "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
# service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
# ============================================================ #
# Login credentials
email = "mahekh@gmail.com"
password = "mahekh2002"
# List of companies to download data for
company_names = ['RELIANCE', 'HDFCLIFE', 'LICHSGFIN', 'BIRLACORPN']
try:
   # Navigate to Screener login page
   driver.get("https://www.screener.in/login/")
   time.sleep(5)
   driver.fullscreen_window()
   # Log in to Screener
   email_input = driver.find_element(By.XPATH, '//*[@id="id_username"]')
   email_input.send_keys(email)
   password_input = driver.find_element(By.XPATH, '//*[@id="id_password"]')
   password_input.send_keys(password)
   password_input.send_keys(Keys.RETURN)
   time.sleep(5)
   # Loop through each company to download data
   for comp_name in company_names:
       driver.get(f"https://www.screener.in/company/{comp_name}/consolidated/")
       time.sleep(12)
       export_csv_button = WebDriverWait(driver, 100).until(
           EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-download", " " ))]'))
       )
       export_csv_button.click()
       time.sleep(15)
   # Verify downloaded files
   download_dir = current_dir
   print("Files in download directory before wait:", os.listdir(download_dir))
finally:
   # Clean up and close the browser
   driver.quit()
