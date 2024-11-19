import pandas as pd

# Set Grocery Items Inventory Excel file's location then read
file_path = 'Resources/Inventory.xlsx'
df = pd.read_excel(file_path)
# df = pd.read_excel(file_path, sheet_name='Sheet1') *** [If multiple sheets]

# Display Excel file contents
print(df)

# Test Printing
print("Lucky 9")

# User input to end program
sayonara = input("Enter any key to exit...")