#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
import os, sys
from tkinter import *
from decimal import Decimal
from datetime import datetime
from mysql.connector import Error
from mysql.connector import (connection)

#--- MAIN WINDOW -------------------------------------------------------------------------------------------------
# Define Classes
class ShoppingCartSystem(Tk):
    # Initialize User Variables
    user_id = None
    user_type = None
    user_name = None
    # Initialize Order Variables
    orderlist_counters = {}
    orderlist_images = []
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
        self.frame_sub = frame_login(self)
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
        self.db_disconnect
        # Assign user values
        self.user_id = self.row_item[0]
        self.user_type = self.row_item[3]
        self.user_name = self.row_item[4]
        print(f"Successfully Logged in user \'{self.user_name}\' with user id \'{self.user_id}\'")
        self.frame_main = frame_header(self)
        self.frame_main.pack()
        # Load user home frame
        if self.user_type == 0:
            self.frame_sub = frame_admin_home(self)
        elif self.user_type == 1:
            self.frame_sub = frame_cust_home(self)
        # Add frame to window
        self.frame_sub.pack(fill=BOTH, expand=1)

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
class frame_mainheader(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Brand Intro Banner
        self.image_banner = PhotoImage(file=parent.path_mainbanner)
        self.label_banner = Label(self, image=self.image_banner)
        self.label_banner.pack()
        self.image_brand = PhotoImage(file=parent.path_mainbrand)
        self.label_brand = Label(self, image=self.image_brand)
        self.label_brand.place(x=412,y=0)
        self.label_brand.lift()

# Dali 9 Brand Conventional Header Frame
class frame_header(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Brand Intro Banner
        self.image_banner = PhotoImage(file=parent.path_banner)
        self.label_banner = Label(self, image=self.image_banner)
        self.label_banner.pack()
        self.image_brand = PhotoImage(file=parent.path_brand)
        self.label_brand = Label(self, image=self.image_brand)
        self.label_brand.place(x=35,y=0)
        self.label_brand.lift()
        # Logout Button
        self.button_logout = Button(self, text = "LOG OUT", fg="white", bg="red", command=lambda: parent.logout())
        self.button_logout.place(x=950,y=2)
        # Welcome Text
        if parent.user_type == 1: # Customer
            self.welcometext = "\"Dali-an niyo umorder...\" "
        elif parent.user_type == 0: # Administrator
            self.welcometext = "\"Dali-an mo mag-manage!\" "
        self.label_welcometext = Label(self, text=self.welcometext, fg="white", bg="#A21F6A", font=("Tahoma", 32, "italic"))
        self.label_welcometext.place(x=230,y=60)

    # Initiate Grocery Cart Feature
    def initiatecart(self):
        # Initialize Grocery Cart Button Image and Cart Items counter
        self.image_cart = PhotoImage(file=self.parent.path_cart)
        self.button_cart = Button(self, image=self.image_cart, command=lambda: self.cart_view())
        self.button_cart.place(x=800,y=33)
        self.button_cart.lift()
        self.label_cartcount = Label(self, text="(XX items)", fg="white", bg="#A21F6A", justify="center", font=("Tahoma", 16, ""))
        self.label_cartcount.place(x=852,y=112)
        # Load Ongoing Order
        for self.row in self.parent.rows_orders:
            # Load unfinished Order
            if (self.row[1] == self.parent.user_id and self.row[4] != True):
                self.parent.row_order = self.row
                print(f"    Retrieved order number \'{self.parent.row_order[0]}\' for user \'{self.parent.user_id}\'.")
        # Create New Order if all user's orders are finished or no orders exist in database
        if (self.parent.row_order == None):
            self.cursor = self.parent.connection.cursor()
            self.query = "INSERT INTO orders (id_user, datetime_initiate) VALUES (%s, %s)"
            self.cursor.execute(self.query, (self.parent.user_id, datetime.now()))
            self.parent.connection.commit()
            print("Created new user Order.")
        # Update Grocery Cart items count
        self.parent.update_orderitems()

    # Grocery Cart Popup Window
    def cart_view(self):
        # Intiialize Cart Summary popup window
        self.cart = Toplevel(self.parent)
        self.cart.focus_set()
        self.cart.grab_set()
        # Set Cart Summary popup window's properties and center position to screen
        self.cart.title("Cart Summary and Checkout")
        self.cart.iconbitmap(self.parent.path_icon)
        self.cart.resizable(False, False)
        self.window_height = 500
        self.window_width = 470
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/2))
        self.cart.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))
        # Initialize Canvas
        self.canvas = Canvas(self.cart)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Initialize Scrollbar
        self.scrollbar = Scrollbar(self.cart, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # Configure Canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        # Initialize internal Frame into an internal Window within the Canvas
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        # Bind mouse wheel event
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<MouseWheel>", self.set_mousewheel(self.canvas, self.on_mousewheel))
        # Define Receipt Grid text values
        self.text000 = ("\n"
            "DALI 9: LUCKY 9 (PBSP INC.)\n"
            "ACCENTURE INC., Q.C. LGU, EDULYNX CORP.\n"
            "METRO MANILA, NCR, MANILA, PHILIPPINES\n"
            "VAT REG TIN: 0100-034-694-001\n"
            "SN: 185042801632\n"
            "MIN:19031317134025685\n"
        )
        self.text00 = "ORDER INVOICE\n"
        self.text10 = (
            "Terminal\n"
            "SI\n"
            "Order #\n"
            "Customer\n"
            "Initiated"
        )
        self.text11 = ":\n:\n:\n:\n:"
        self.text12 = (
            "NHT-NIT\n"
            "Batch-04\n"
            f"{self.parent.row_order[0]}\n"
            f"{self.parent.user_name}-{self.parent.row_order[1]}\n"
            f"{self.parent.row_order[2]}"
        )
        self.text20 = "------------------------------------------------------------------------"
        # Traverse order list items for active order
        if self.parent.rows_orderitems != []:
            self.text30 = ""
            self.text31 = ""
            # Traverse current order items
            for self.orderitem in self.parent.rows_orderitems:
                # Compare to each inventory item to retrieve item name and price
                for self.item in self.parent.rows_items:
                    # If item id matches
                    if self.item[0] == self.orderitem[1]:
                        # Retrieve name
                        self.text30 = f"{self.text30}\n{self.item[1].upper()}"
                        # If item quantity > 1, subtotal price
                        if self.orderitem[2] > 1:
                            self.text30 = f"{self.text30}\n\t{self.orderitem[2]} X\t{self.item[3]}"
                            self.text31 = f"{self.text31}\n\n{self.orderitem[2]*self.item[3]}"
                        # Otherwise, retrieve retail price
                        else:
                            self.text31 = f"{self.text31}\n{self.item[3]}"
        else:
            self.text30 = "Order List for active order is empty."
        self.text40 = "------------------------------------------------------------------------"
        self.text50 = self.parent.total_quantity
        self.text51 = "Item(s)"
        self.text52 = f"Php {self.parent.row_order[5]}"
        self.text60 = "--------------"
        self.text70 = ("\n"
            "VATABLE SALES\n"
            "Total Sales\n"
            "VAT AMOUNT (12%)"
        )
        self.text71 = "\n:\n:\n:"
        self.tax = round(self.parent.row_order[5]*Decimal(0.12), 2)
        self.text72 = ("\n"
            f"{self.parent.row_order[5]-self.tax}\n"
            f"{self.parent.row_order[5]-self.tax}\n"
            f"{self.tax}"
        )
        self.text80 = "Total Amount\n\n" #placeholder
        self.text81 = ":\n\n" #placeholder
        self.text82 = f"{self.parent.row_order[5]}\n\n" #placeholder
        # Format Receipt Grid and assign text values
        self.fontsize = 14
        self.fontstyle = "Arial"
        self.maxcolumns = 4
        # Section 1 (Header)
        Label(self.frame, text=self.text000, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=0, column=0, columnspan=self.maxcolumns)
        Label(self.frame, text=self.text00, font=(self.fontstyle, self.fontsize, "bold"), fg="black").grid(row=1, column=0, columnspan=self.maxcolumns)
        # Section 2 (Order Details)
        Label(self.frame, text=self.text10, font=(self.fontstyle, self.fontsize, ""), justify=LEFT, fg="black").grid(row=2, column=0, sticky=W)
        Label(self.frame, text=self.text11, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=2, column=1, sticky=W, columnspan=2)
        Label(self.frame, text=self.text12, font=(self.fontstyle, self.fontsize, ""), justify=LEFT, fg="black").grid(row=2, column=3, sticky=W)
        # Section 3 (Divider)
        Label(self.frame, text=self.text20, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=3, column=0, columnspan=self.maxcolumns)
        # Section 4 (Order Items)
        if self.parent.rows_orderitems == []:
            Label(self.frame, text=self.text30, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=4, column=0, columnspan=self.maxcolumns)
        else:
            Label(self.frame, text=self.text30, font=(self.fontstyle, self.fontsize, ""), justify=LEFT, fg="black").grid(row=4, column=0, sticky=W, columnspan=3)
            Label(self.frame, text=self.text31, font=(self.fontstyle, self.fontsize, ""), justify=RIGHT, fg="black").grid(row=4, column=3, sticky=E)
        # Section 5 (Divider)
        Label(self.frame, text=self.text40, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=5, column=0, columnspan=self.maxcolumns)
        # Section 6 (Quantity and Price Totals)
        Label(self.frame, text=self.text50, font=(self.fontstyle, self.fontsize, "bold"), justify=LEFT, fg="black").grid(row=6, column=0)
        Label(self.frame, text=self.text51, font=(self.fontstyle, self.fontsize, ""), justify=LEFT, fg="black").grid(row=6, column=1, sticky=W)
        Label(self.frame, text=self.text52, font=(self.fontstyle, self.fontsize, "bold"), justify=RIGHT, fg="black").grid(row=6, column=2, sticky=E, columnspan=2)
        # Section 7 (Subdivider)
        Label(self.frame, text=self.text60, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=7, column=0, stick=E, columnspan=self.maxcolumns)
        # Section 8 (VAT)
        Label(self.frame, text=self.text70, font=(self.fontstyle, self.fontsize, ""), justify=LEFT, fg="black").grid(row=8, column=0, sticky=W)
        Label(self.frame, text=self.text71, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=8, column=1, sticky=W)
        Label(self.frame, text=self.text72, font=(self.fontstyle, self.fontsize, ""), justify=RIGHT, fg="black").grid(row=8, column=2, sticky=W, columnspan=2)
        # Section 9 (Total)
        Label(self.frame, text=self.text80, font=(self.fontstyle, self.fontsize, "bold"), justify=LEFT, fg="black").grid(row=9, column=0, sticky=W)
        Label(self.frame, text=self.text81, font=(self.fontstyle, self.fontsize, "bold"), fg="black").grid(row=8, column=9, sticky=W)
        Label(self.frame, text=self.text82, font=(self.fontstyle, self.fontsize, "bold"), justify=RIGHT, fg="black").grid(row=9, column=2, sticky=W, columnspan=2)
        # Section 10 
    # Mouse Scroll Wheel event
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # Activate/Deactivate mousewheel scrolling when mouse cursor is over/not over the respective widget
    def set_mousewheel(self, widget, command):
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))

#--- USER ACCESS FRAMES --------------------------------------------
# Login Frame
class frame_login(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # User Login/Registration +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.temp_cust = Button(self, text = "Customer", font=("Tahoma", 30, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(1)) #pass user id in param
        self.temp_cust.pack(pady=60)
        self.temp_mana = Button(self, text = "Administrator", font=("Tahoma", 30, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(0)) #pass user id in param
        self.temp_mana.pack(pady=20)
        # verify user's username and password then pass value to user_authorization()
        #placeholder

# Registration Frame
# placeholder
# exit program to "return" to login frame

#--- CUSTOMER USER FRAMES ------------------------------------------
# Customer Frame: Home
class frame_cust_home(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Initialize Canvas
        self.canvas = Canvas(parent)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Initialize Scrollbar
        self.scrollbar = Scrollbar(parent, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # Configure Canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        # Initialize internal Frame into an internal Window within the Canvas
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        # Bind mouse wheel event
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<MouseWheel>", self.set_mousewheel(self.canvas, self.on_mousewheel))
        # Open Database Connection
        parent.db_connect("announce")
        self.cursor = parent.connection.cursor()
        # Access Database: Retrieve "inventory" table rows data
        self.cursor.execute("SELECT * FROM inventory")
        parent.rows_items = self.cursor.fetchall()
        print(f"    Retrieved \'{len(parent.rows_items)}\' rows from \"inventory\" table.")
        # Access Database: Retrieve "orders" table rows data
        self.cursor.execute("SELECT * FROM orders")
        parent.rows_orders = self.cursor.fetchall()
        print(f"    Retrieved \'{len(parent.rows_orders)}\' rows from \"orders\" table.")
        # Initiate Cart Button
        parent.frame_main.initiatecart()
        # Close Database Connection
        parent.db_disconnect("announce")
        # Initialize Grocery inventory rows header titles
        Label(self.frame, text="IMAGE", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=0, pady=10, padx=0)
        Label(self.frame, text="NAME", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=1, pady=10, padx=0)
        Label(self.frame, text="QUANTITY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=2, pady=10, padx=0)
        Label(self.frame, text="PRICE", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=3, pady=10, padx=0)
        Label(self.frame, text="CATEGORY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=4, pady=10, padx=0)
        Label(self.frame, text="").grid(row=0, column=5, pady=10, padx=10)
        Label(self.frame, text="").grid(row=0, column=6, pady=10, padx=10)
        Label(self.frame, text="ORDERED", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=7, pady=10, padx=0)
        # Display retrieved "inventory" table rows
        self.item_placeholder = PhotoImage(file=parent.resource_path("resources/placeholder.png"))
        self.rowcounter = 0
        for self.row in parent.rows_items:
            self.rowcounter += 1
            # If 'imagepath' value is empty
            if self.row[5] == "":
                self.item_image = self.item_placeholder
            else:
                self.item_image = PhotoImage(file=parent.resource_path(self.row[5]))
                parent.orderlist_images.append(self.item_image)
            # image
            self.label_image = Label(self.frame, image=self.item_image)
            self.label_image.grid(row=self.rowcounter, column=0, padx=5)
            # name
            Label(self.frame, text=self.row[1], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=1, pady=0, padx=0)
            # quantity
            Label(self.frame, text=self.row[2], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=2, pady=0, padx=0)
            # price
            Label(self.frame, text=f"Php {self.row[3]}", font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=3, pady=0, padx=0)
            # category
            Label(self.frame, text=self.row[4], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=4, pady=0, padx=23)
            # order buttons
            Button(self.frame, text="Order", font=("Tahoma", 12, "bold"), fg="white", bg="green", command=lambda item=self.row[0]: self.item_add(item)).grid(row=self.rowcounter, column=5, pady=0, padx=0)
            Button(self.frame, text="-", font=("Tahoma", 12, "bold"), fg="white", bg="red", command=lambda item=self.row[0]: self.item_remove(item)).grid(row=self.rowcounter, column=6, pady=0, padx=5)
            # order counter labels
            self.label_counter = Label(self.frame, text="- - -", font=("Tahoma", 16, ""))
            self.label_counter.grid(row=self.rowcounter, column=7, pady=0, padx=0)
            parent.orderlist_counters[self.rowcounter-1] = self.label_counter
        # Initialize item order list counters
        parent.db_connect()
        self.rowcounter = 0
        # Traverse entire Grocery Inventory
        for self.row in parent.rows_items:
            # Check if Grocery item matches an ordered item
            self.cursor = self.parent.connection.cursor()
            self.cursor.execute(f"SELECT * FROM orderitems WHERE id_order = {self.parent.row_order[0]} AND id_item = {self.row[0]}")
            self.row_item = self.cursor.fetchone()
            # Change corresponding Grocery item's Label counter
            if self.row_item != None:
                parent.orderlist_counters[self.rowcounter].config(text=self.row_item[2])
            self.rowcounter += 1
        parent.db_disconnect()
    # Mouse Scroll Wheel event
    def on_mousewheel(self, event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # Activate/Deactivate mousewheel scrolling when mouse cursor is over/not over the respective widget
    def set_mousewheel(self, widget, command):
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))
    # Add item to order list
    def item_add(self, item):
        # Access Database: Insert row to "orderitems" table
        self.parent.db_connect()
        # Check if item is already listed
        self.cursor = self.parent.connection.cursor()
        self.cursor.execute(f"SELECT * FROM orderitems WHERE id_order = {self.parent.row_order[0]} AND id_item = {item}")
        self.row_item = self.cursor.fetchone()
        self.cursor = self.parent.connection.cursor()
        # Update table row for existing ordered item
        if self.row_item != None:
            self.query = ("UPDATE orderitems SET quantity = %s WHERE id_order = %s AND id_item = %s")
            self.data = (self.row_item[2]+1, self.row_item[0], self.row_item[1])
            print(f"    Increased item id \'{item}\' quantity to \'{self.row_item[2]+1}\'.")
        # Insert row to database
        else:
            self.query = "INSERT INTO orderitems (id_order, id_item, quantity) VALUES (%s, %s, %s)"
            self.data = (self.parent.row_order[0], item, 1)
            print(f"    Added item id \'{item}\' to order.")
        # Apply Change
        self.cursor.execute(self.query, self.data)
        self.parent.connection.commit()
        # Update order list items then close Database Connection
        self.parent.update_orderitems()
        self.parent.db_disconnect()
    # Remove item from order list
    def item_remove(self, item):
        # Access Database: Remove row from "orderitems" table
        self.parent.db_connect()
        # Check if item is already listed
        self.cursor = self.parent.connection.cursor()
        self.cursor.execute(f"SELECT * FROM orderitems WHERE id_order = {self.parent.row_order[0]} AND id_item = {item}")
        self.row_item = self.cursor.fetchone()
        if self.row_item != None:
            self.cursor = self.parent.connection.cursor()
            # Update table row for item quantity change
            if self.row_item[2] > 1:
                self.query = ("UPDATE orderitems SET quantity = %s WHERE id_order = %s AND id_item = %s")
                self.data = (self.row_item[2]-1, self.row_item[0], self.row_item[1])
                print(f"    Decreased item id \'{item}\' quantity to \'{self.row_item[2]-1}\'.")
            # Remove row from database
            else:
                self.query = "DELETE FROM orderitems WHERE id_order = %s AND id_item = %s"
                self.data = (self.parent.row_order[0], item)
                print(f"    Removed item id \'{item}\' from order.")
            # Apply Change
            self.cursor.execute(self.query, self.data)
            self.parent.connection.commit()
        else:
            print(f"    Item id \'{item}\' not listed in order.")
        # Update order list items then close Database Connection
        self.parent.update_orderitems()
        self.parent.db_disconnect()

#--- ADMINISTRATOR USER FRAMES -------------------------------------
# Administrator Frame: Home
class frame_admin_home(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        #placeholder
        self.labeltemp = Label(self, text="placeholder")
        self.labeltemp.pack()
        
#-----------------------------------------------------------------------------------------------------------------
#--- RUNTIME INITIATE --------------------------------------------------------------------------------------------
# Define and Instantiate Shopping Cart App 
ShoppingCartSystem().mainloop()

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------