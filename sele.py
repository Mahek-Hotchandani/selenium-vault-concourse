from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import time
# Setup Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Path to the ChromeDriver you installed
driver = webdriver.Chrome(options=chrome_options)
# URL to scrape
url = 'https://screener.in/company/RELIANCE/consolidated/'
# Open the webpage
driver.get(url)
time.sleep(5)  # Wait for the page to fully load
# Locate the profit-loss table section by ID
profit_loss_section = driver.find_element(By.ID, "profit-loss")
# Locate the table within the section
table = profit_loss_section.find_element(By.TAG_NAME, "table")
# Extract table data
table_data = []
rows = table.find_elements(By.TAG_NAME, "tr")
for row in rows:
   row_data = []
   cells = row.find_elements(By.TAG_NAME, "th") + row.find_elements(By.TAG_NAME, "td")
   for cell in cells:
       row_data.append(cell.text.strip())
   table_data.append(row_data)
# Convert the table data to a DataFrame
df_table = pd.DataFrame(table_data)
# Rename the first cell in the first row
df_table.iloc[0, 0] = 'Section'
# Set the first row as column names
df_table.columns = df_table.iloc[0]
# Remove the first row from DataFrame
df_table = df_table[1:]
# Transpose the DataFrame
df_table = df_table.transpose().reset_index()
df_table.columns = df_table.iloc[0]  # Set new column names
df_table = df_table[1:]  # Remove the old header row
# Reset index and add primary key
df_table.reset_index(drop=True, inplace=True)
df_table.index += 1
df_table.index.name = 'id'
df_table.reset_index(inplace=True)
# Ensure only valid numeric data is processed with eval
def safe_eval(val):
   try:
       return eval(val)
   except:
       return val
# Convert relevant columns to numeric types
for i in df_table.columns[1:]:
   df_table[i] = df_table[i].str.replace(',', '').str.replace('%', '/100').apply(safe_eval)
# PostgreSQL database connection details
db_params = {
   'dbname': 'reliance_profitloss',
   'user': 'mahek',
   'password': 'mahek',
   'host': '192.168.3.185',
   'port': 5432
}
# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cur = conn.cursor()
# Create table if not exists
create_table_query = '''
CREATE TABLE IF NOT EXISTS profit_loss_data (
  Index BIGINT primary key,
  Year TEXT,
  Sales BIGINT,
  Expenses BIGINT,
  Operating_Profit BIGINT,
  OPM_Percent DOUBLE PRECISION,
  Other_Income BIGINT,
  Interest BIGINT,
  Depreciation BIGINT,
  Profit_before_tax BIGINT,
  Tax_Percent DOUBLE PRECISION,
  Net_Profit BIGINT,
  EPS_in_Rs DOUBLE PRECISION,
  Dividend_Payout_Percent INTEGER
);
'''
cur.execute(create_table_query)
conn.commit()
# Clear table before inserting new data
clear_table_query = 'TRUNCATE TABLE profit_loss_data;'
cur.execute(clear_table_query)
conn.commit()
# Insert data into the PostgreSQL table
insert_query = '''
INSERT INTO profit_loss_data (
  Index, Year, Sales, Expenses, Operating_Profit, OPM_Percent, Other_Income, Interest, Depreciation,
  Profit_before_tax, Tax_Percent, Net_Profit, Dividend_Payout_Percent, EPS_in_Rs
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (Index) DO UPDATE SET
  Year = EXCLUDED.Year,
  Sales = EXCLUDED.Sales,
  Expenses = EXCLUDED.Expenses,
  Operating_Profit = EXCLUDED.Operating_Profit,
  OPM_Percent = EXCLUDED.OPM_Percent,
  Other_Income = EXCLUDED.Other_Income,
  Interest = EXCLUDED.Interest,
  Depreciation = EXCLUDED.Depreciation,
  Profit_before_tax = EXCLUDED.Profit_before_tax,
  Tax_Percent = EXCLUDED.Tax_Percent,
  Net_Profit = EXCLUDED.Net_Profit,
  Dividend_Payout_Percent = EXCLUDED.Dividend_Payout_Percent,
  EPS_in_Rs = EXCLUDED.EPS_in_Rs;
'''
for _, row in df_table.iterrows():
   cur.execute(insert_query, tuple(row))
   conn.commit()  # Commit after each insert
   print(f"Inserted data for year: {row['id']}")
   time.sleep(3)
# Close the connection
cur.close()
conn.close()
# Close the browser
driver.quit()