import pandas as pd
import openpyxl
import os

def read_profit_and_loss_tab(file_name):   
    if file_name:
        try:
            # Load only the "Profit and Loss" sheet
            profit_and_loss_df = pd.read_excel(file_name, sheet_name="Data Sheet" , usecols='A:K' , skiprows=15 , nrows=15)
            # print(profit_and_loss_df)
            # Perform any additional processing here if needed
            profit_and_loss_df.set_index("Report Date" , inplace=True)
            # print(profit_and_loss_df)
            profit_and_loss_df = profit_and_loss_df.transpose()
            profit_and_loss_df["company"] = file_name.strip(".xlsx")

            print(f"Profit and Loss Data {file_name}:")
            print(profit_and_loss_df)

            try:
                profit_and_loss_df.to_csv('profit_loss.csv', mode='x' , index=True, header=True)
            except FileExistsError:
                profit_and_loss_df.to_csv('profit_loss.csv', mode='a', index=True, header=False)

        except Exception as e:
            print(f"Error reading Excel file or extracting Profit and Loss tab: {e}")
    else:
        print(f"File {file_name} not found")

if __name__ == '__main__':
    file_name = "Reliance Industr.xlsx"
    read_profit_and_loss_tab(file_name)
