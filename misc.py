''' --------------------------------------------------------------------------------------------------- '''
# User input to end program
sayonara = input("Enter any key to exit...")

''' --------------------------------------------------------------------------------------------------- '''
# ---------------------------------------------------------------------------------------------------
'''Nuitka Building
nuitka --standalone --output-dir=build --include-data-dir=resources=resources --windows-icon-from-ico=resources/logo_icon.ico --enable-plugin=tk-inter --include-package=mysql.connector --include-package=login --include-package=user_custo --include-package=user_custo_header --include-package=user_admin main.py

--onefile
--standalone 
--include-data-file=resources/puregro.ico=resources/puregro.ico
--include-data-files=resources/*.png=resources

--standalone: Creates a standalone application, including all necessary dependencies.
--onefile: Packages everything into a single executable file.
--output-dir=dist: Specifies the directory where the output file will be stored.

To include the resources/ directory:
nuitka --standalone --onefile --include-data-dir=resources=resources app.py
To include individual files:
nuitka --standalone --onefile --include-data-file=resources/config.json=resources/config.json 
       --include-data-file=resources/logo.png=resources/logo.png app.py

Adding an icon:
nuitka --standalone --onefile --windows-icon-from-ico=icon.ico app.py
Optimizing for performance:
nuitka --standalone --onefile --lto --follow-imports app.py
'''
# ---------------------------------------------------------------------------------------------------
''' Database Connection
import pandas as pd
from mysql.connector import (connection)
from mysql.connector import Error
# Step 1: Read the Excel file
file_path = "resources/Inventory.xlsx"
df = pd.read_excel(file_path)
# Step 2: Connect to the MySQL database
try:
    connection = connection.MySQLConnection(
        host="127.0.0.1",
        user="root",
        password="",
        database="dali_9"
    )
    if connection.is_connected():
        print("Connected to the database")
        # Step 3: Create a cursor object
        cursor = connection.cursor()
        # Step 4: Iterate through the DataFrame and insert rows into the database
        for _, row in df.iterrows():
            sql_query = """
            INSERT INTO inventory (name, quantity, price, category, barcode)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (row['Item'], row['Weight'], row['Price'], row['Category'], row['Barcode'])  # Adjust column names
            cursor.execute(sql_query, data)
        # Commit the transaction
        connection.commit()
        print(f"{cursor.rowcount} rows inserted successfully.")
except Error as e:
    print("Error while connecting to MySQL:", e)
finally:
    # Step 5: Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
'''
# ---------------------------------------------------------------------------------------------------
''' Python Debugger
You can launch a Python program through pdb via python -m pdb myscript.py.

There are a few commands you can then issue, which are documented on the pdb page.

Some useful ones to remember are:

b: set a breakpoint
c: continue debugging until you hit a breakpoint
s: step through the code
n: to go to next line of code
l: list source code for the current file (default: 11 lines including the line being executed)
u: navigate up a stack frame
d: navigate down a stack frame
p: to print the value of an expression in the current context
'''
# ---------------------------------------------------------------------------------------------------
''' Excel File Reader
import pandas as pd

# Set Grocery Items Inventory Excel file's location then read
file_path = 'Resources/Inventory.xlsx'
df = pd.read_excel(file_path)
# df = pd.read_excel(file_path, sheet_name='Sheet1') *** [If multiple sheets]

# Display Excel file contents
print(df)
'''
# ---------------------------------------------------------------------------------------------------
''' Main Class Code Zero
class App(Tk):
    def __init__(self):
        super().__init__()

        # Initialize window properties
        self.title("Puregro Shopping Cart")
        self.iconbitmap('resources/puregro.ico')
        self.geometry('700x450')

        # Variables
        self.status = True

        # Widgets
        self.my_label = Label(self, text="Hello World!", font=("Helvetica", 42))
        self.my_label.pack(pady=20)

        self.my_button = Button(self, text = "Change Text", command=self.change)
        self.my_button.pack(pady=20)

    def change(self):
        if self.status == True:
            self.my_label.config(text="Goodbye World!")
            self.status = False
        else:
            self.my_label.config(text="Hello World!")
            self.status = True
'''
# ---------------------------------------------------------------------------------------------------
'''
To store PNG files (or any binary data like images) in MySQL, you should use a BLOB (Binary Large Object) data type.
The BLOB type is designed to store large amounts of binary data, such as images, audio, or any other files.
There are several types of BLOB in MySQL, and the most common ones are:
TINYBLOB: Can store up to 255 bytes.
BLOB: Can store up to 65,535 bytes (64 KB).
MEDIUMBLOB: Can store up to 16,777,215 bytes (16 MB).
LONGBLOB: Can store up to 4,294,967,295 bytes (4 GB).
'''
# ---------------------------------------------------------------------------------------------------