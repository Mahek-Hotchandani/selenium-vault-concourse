import pandas as pd
import openpyxl
import os
from sqlalchemy import create_engine
def read_profit_and_loss_tab(file_name):
   if file_name:
       try:
           # Load only the "Profit and Loss" data from the "Data Sheet"
           profit_and_loss_df = pd.read_excel(file_name, sheet_name="Data Sheet", usecols='A:K', skiprows=15, nrows=15)
           # Set 'Report Date' as the index
           profit_and_loss_df.set_index("Report Date", inplace=True)
           # Transpose the data (rows become columns and columns become rows)
           profit_and_loss_df = profit_and_loss_df.transpose()
           # Add a new column 'company' by stripping the '.xlsx' extension from the file name
           profit_and_loss_df["company"] = file_name.strip(".xlsx")
           print(f"Profit and Loss Data from {file_name}:")
           print(profit_and_loss_df)
           # Append the data to the CSV file
           try:
               profit_and_loss_df.to_csv('profit_loss.csv', mode='x', index=True, header=True)
           except FileExistsError:
               profit_and_loss_df.to_csv('profit_loss.csv', mode='a', index=True, header=False)
           # Connect to PostgreSQL database and send the data
           engine = create_engine('postgresql://mahek:mahek@192.168.3.185/reliance_profitloss')
           profit_and_loss_df.to_sql('profit_loss_data', engine, if_exists='append', index=True)
           print(f"Data from {file_name} successfully loaded into PostgreSQL")
       except Exception as e:
           print(f"Error reading Excel file or extracting Profit and Loss data: {e}")
   else:
       print(f"File {file_name} not found")
if __name__ == '__main__':
   # List of Excel files
   company_files = ["Reliance Industr.xlsx", "Birla Corpn.xlsx", "HDFC Life Insur.xlsx", "LIC Housing Fin.xlsx"]
   # Loop through each file and process it
   for file_name in company_files:
       file_path = os.path.join(file_name)
       read_profit_and_loss_tab(file_path)
