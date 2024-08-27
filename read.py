import pandas as pd
import openpyxl
import os

def read_profit_and_loss_tab(file_name):
    # Check if the file exists
    if file_name and os.path.exists(file_name):
        try:
            # Load the Excel file
            workbook = openpyxl.load_workbook(file_name, data_only=True)

            # Refresh all data connections manually (if needed)
            # openpyxl does not support refreshing data connections
            # If your Excel requires external refresh, consider updating data manually or from source

            # Load only the "Profit and Loss" sheet into a DataFrame
            profit_and_loss_df = pd.read_excel(file_name, sheet_name="Profit & Loss", engine='openpyxl')

            # Display the first few rows
            print("Profit and Loss Data:")
            print(profit_and_loss_df.head(13))

        except Exception as e:
            print(f"Error reading Excel file or extracting Profit and Loss tab: {e}")
    else:
        print(f"File {file_name} not found or path is incorrect.")

if __name__ == '__main__':
    file_name = "Reliance Industr.xlsx"
    read_profit_and_loss_tab(file_name)
