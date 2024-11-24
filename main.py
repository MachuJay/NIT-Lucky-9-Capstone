# Import packages
from tkinter import *
import os, sys
from mysql.connector import (connection)
from mysql.connector import Error

# Define Classes
class ShoppingCartSystem(Tk):
    def __init__(self):
        super().__init__()

        #Initialize resources items paths
        self.path_icon = self.resource_path("resources/logo_icon.ico")
        self.path_brand = self.resource_path("resources/logo_brand.png")
        self.path_banner = self.resource_path("resources/logo_banner.png")

        # Initialize window properties
        self.title("Dali 9 Shopping Cart System")
        self.iconbitmap(self.path_icon)
        self.resizable(False, False)

        # Center program window on screen
        self.window_height = 720
        self.window_width = 1024
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/2))
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))

        # Load: Header Frame
        frame_primary = frame_header(self)
        frame_primary.pack()

        # Load: Login Frame
        #placeholder

        '''
        self.togglestatus = True
        self.my_button = Button(self, text = "Toggle", command=self.change)
        self.my_button.pack(pady=20)
        '''

    # Get the absolute path to a resource file (Works in dev and built modes)
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            # Running as an executable
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

# Dali 9 Brand Header Frame
class frame_header(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Brand Intro Banner
        self.image_banner = PhotoImage(file=self.parent.path_banner)
        self.label_banner = Label(self, image=self.image_banner)
        self.label_banner.pack()
        self.image_brand = PhotoImage(file=self.parent.path_brand)
        self.label_brand = Label(self, image=self.image_brand)
        self.label_brand.place(x=412,y=0)
        self.label_brand.lift()

# Define and Instantiate Shopping Cart App 
ShoppingCartSystem().mainloop()

'''
# Connection Test
try:
    self.connection = connection.MySQLConnection(
        host='127.0.0.1',
        user='root',
        password='',
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
except Error as e:
    print("Error while connecting to MySQL:", e)
finally:
    # Step 6: Close the connection
    if self.connection.is_connected():
        self.cursor.close()
        self.connection.close()
        print("MySQL connection closed")
'''