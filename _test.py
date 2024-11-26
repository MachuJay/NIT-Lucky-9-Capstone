from mysql.connector import (connection)
from mysql.connector import Error

try:
    connection = connection.MySQLConnection(user='root', password='',
                                    host='127.0.0.1',
                                    database='dali_9')

    if connection.is_connected():
            print("Connected to the database")
            # Step 2: Create a cursor object
            cursor = connection.cursor()

            # Step 3: Execute the SQL query to fetch all rows
            query = "SELECT * FROM inventory;"
            cursor.execute(query)

            # Step 4: Fetch all rows from the query result
            rows = cursor.fetchall()

            # Step 5: Display the results
            print("Contents of the table 'INVENTORY':")
            for row in rows:
                print(row)
            
            x = input("\n\nProceed?")

except Error as e:
    print("Error while connecting to MySQL:", e)
finally:
    # Step 6: Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")

'''
        # Connection Test
        try:
            self.connection = connection.MySQLConnection(user='root', password='',
                                            host='127.0.0.1',
                                            database='dali_9')

            if self.connection.is_connected():
                print("Connected to the database")
                # Step 2: Create a cursor object
                self.cursor = self.connection.cursor()

                # Step 3: Execute the SQL query to fetch all rows
                query = "SELECT * FROM inventory;"
                self.cursor.execute(query)

                # Step 4: Fetch all rows from the query result
                rows = self.cursor.fetchall()

                # Step 5: Display the results
                print("Contents of the table 'INVENTORY':")
                for row in rows:
                    print(row)
                
                x = input("\n\nProceed?")

        except Error as e:
            print("Error while connecting to MySQL:", e)
        finally:
            # Step 6: Close the connection
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection closed")
'''



'''
# Label Box
self.my_label = Label(self, text="Hello Lucky 9!", font=("Helvetica", 42))
self.my_label.pack(pady=20)

# Toggle Button
self.togglestatus = True
self.my_button = Button(self, text = "Toggle", command=self.change)
self.my_button.pack(pady=20)
# Toggle Button Action
def change(self):
    if self.togglestatus == True:
        self.my_label.config(text="GUI App Initialized.")
        self.togglestatus = False
    else:
        self.my_label.config(text="Hello Lucky 9!")
        self.togglestatus = True
'''