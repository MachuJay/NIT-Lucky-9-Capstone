#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
import os, sys
import login
import user_custo, user_admin
import user_custo_header
import tkinter as tk
from mysql.connector import Error
from mysql.connector import (connection)

#--- MAIN WINDOW -------------------------------------------------------------------------------------------------
# Define Classes
class ShoppingCartSystem(tk.Tk):
    # Initialize User Variables
    user_id = None
    user_type = None
    user_name = None
    # Initialize Order Variables
    orderlist_counters = {}
    orderlist_images = []
    adminlist_prices = {}
    total_quantity = None
    # Initialize Database Rows
    rows_items = None
    rows_orders = None
    rows_orderitems = None
    # Initialize User Order Database Row
    row_order = None

    def __init__(self):
        super().__init__()

        #Initialize resources items paths
        self.path_icon = self.resource_path("resources/logo_icon.ico")
        self.path_mainbrand = self.resource_path("resources/logo_mainbrand.png")
        self.path_mainbanner = self.resource_path("resources/logo_mainbanner.png")
        self.path_brand = self.resource_path("resources/logo_icon.png")
        self.path_banner = self.resource_path("resources/logo_banner.png")
        self.path_cart = self.resource_path("resources/logo_cart.png")

        # Initialize window properties
        self.title("Dali 9 Shopping Cart System")
        self.iconbitmap(self.path_icon)
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.attributes('-topmost', False)

        # Center program window on screen
        self.window_height = 720
        self.window_width = 1024
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/2))
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))

        # Load: Header Frame
        self.frame_main = frame_mainheader(self)
        self.frame_main.pack()

        # Load: Login Frame
        self.frame_sub = login.frame_login(self)
        self.frame_sub.pack()

        print("\n-------------") # Program CLI Logs Spacing

#--- FUNCTIONS ---------------------------------------------------------------------------------------------------
    # Get the absolute path to a resource file (Works in dev and built modes)
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            # Running as an executable
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    # Set user type variable and load respective home interface 
    def user_authorization(self, id):
        # Remove Login Frame then replace Header Frame 
        self.frame_sub.destroy()
        self.frame_main.destroy()
        # Access Database: Retrieve user row from database
        self.db_connect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        self.row_item = self.cursor.fetchone()
        self.db_disconnect()
        # Assign user values
        self.user_id = self.row_item[0]
        self.user_type = self.row_item[3]
        self.user_name = self.row_item[4]
        print(f"Successfully Logged in user \'{self.user_name}\' with user id \'{self.user_id}\'")
        self.frame_main = user_custo_header.frame_header(self)
        self.frame_main.pack()
        # Load user home Frame
        if self.user_type == 0:
            self.frame_sub = user_admin.frame_admin_home(self)
        elif self.user_type == 1:
            self.frame_sub = user_custo.frame_cust_home(self)
        # Add Frame to window
        self.frame_sub.pack(fill=tk.BOTH, expand=1)

    # Connect to Database
    def db_connect(self, log="silent"):
        try:
            self.connection = connection.MySQLConnection(
                host="127.0.0.1",
                user="root",
                password="",
                database="dali_9"
            )
            if self.connection.is_connected():
                if log == "announce":
                    print(f"Succesfully connected to database \'{self.connection.database}\'")
                self.cursor = self.connection.cursor
        except Error as e:
            print("Error while connecting to MySQL:", e)

    # Disconnect from Database
    def db_disconnect(self, log="silent"):
        if self.connection.is_connected():
            if log == "announce":
                print(f"Succesfully disconnected from database \'{self.connection.database}\'")
            self.connection.close()

    # Update Grocery Cart items count
    def update_orderitems(self):
        # Update Grocery Cart items counter
        self.db_connect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT * FROM orderitems WHERE id_order = {self.row_order[0]}")
        self.rows_orderitems = self.cursor.fetchall()
        self.total_quantity = 0
        for self.row in self.rows_orderitems:
            self.total_quantity += self.row[2]
        self.frame_main.label_cartcount.config(text=f"({self.total_quantity}) items")
        
        # Update item order list counters
        if len(self.orderlist_counters) != 0:
            self.db_connect()
            self.rowcounter = 0
            # Traverse entire Grocery Inventory
            for self.row in self.rows_items:
                # Check if Grocery item matches an ordered item
                self.cursor = self.connection.cursor()
                self.cursor.execute(f"SELECT * FROM orderitems WHERE id_order = {self.row_order[0]} AND id_item = {self.row[0]}")
                self.row_item = self.cursor.fetchone()
                # Change corresponding Grocery item's Label counter
                if self.row_item != None:
                    self.orderlist_counters[self.rowcounter].config(text=self.row_item[2])
                else:
                    self.orderlist_counters[self.rowcounter].config(text="- - -")
                self.rowcounter += 1
            # Update active order's total price
            self.ordertotal = 0
            # Traverse order items list
            for self.row_orderitem in self.rows_orderitems:
                # If Item is listed in active order
                if self.row_orderitem[0] == self.row_order[0]:
                    # Traverse inventory items list to retrieve item price then update total active order price
                    for self.row_item in self.rows_items:
                        if self.row_item[0] == self.row_orderitem[1]:
                            self.subtotal = self.row_item[3] * self.row_orderitem[2]
                            self.ordertotal += self.subtotal
            # Database Access: Commit current order total column update to database
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"UPDATE orders SET total = {self.ordertotal} WHERE id_order = {self.row_order[0]}")
            self.connection.commit()
            # Update local order row
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT * FROM orders WHERE id_order = {self.row_order[0]}")
            self.row_order = self.cursor.fetchone()
            self.db_disconnect()

    # Logout User Account
    def logout(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
#-----------------------------------------------------------------------------------------------------------------
#--- HEADER FRAMES -----------------------------------------------------------------------------------------------
# Dali 9 Brand Header Frame
class frame_mainheader(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Brand Intro Banner
        self.image_banner = tk.PhotoImage(file=parent.path_mainbanner)
        self.label_banner = tk.Label(self, image=self.image_banner)
        self.label_banner.pack()
        self.image_brand = tk.PhotoImage(file=parent.path_mainbrand)
        self.label_brand = tk.Label(self, image=self.image_brand)
        self.label_brand.place(x=412,y=0)
        self.label_brand.lift()
        
#-----------------------------------------------------------------------------------------------------------------
#--- RUNTIME INITIATE --------------------------------------------------------------------------------------------
# Define and Instantiate Shopping Cart App 
ShoppingCartSystem().mainloop()

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------