from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import win32com.client
 
# Email and password variables
email = 'mahekh@gmail.com'
password = 'mahekh2002'
 
# Path to your WebDriver executable
 
# Start the WebDriver in headless mode
options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
 
# Open the website
try:
    driver.get('https://www.screener.in/login/')
 
    # Wait for the page to load
    time.sleep(5)
 
    # Enter email and password
    driver.find_element(By.XPATH, '//*[@id="id_username"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="id_password"]').send_keys(password + Keys.RETURN)
 
    # Wait for login to complete
    time.sleep(5)
 
    # Navigate to the profit-loss section
    driver.get('https://www.screener.in/company/RELIANCE/consolidated/')
 
    # Wait for the page to load
    time.sleep(5)
 
    # Locate and print the profit-loss section
    # You may need to adjust the selector based on the actual HTML structure
    export_csv_button = driver.find_element(By.XPATH, '//*[@id="top"]/div[1]/form/button')
    export_csv_button.click()
    time.sleep(40)
 
# Close the WebDriver
finally:
    driver.quit()



