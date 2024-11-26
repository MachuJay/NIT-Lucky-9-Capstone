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