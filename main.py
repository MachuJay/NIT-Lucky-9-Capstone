#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
import os, sys
from tkinter import *
from datetime import datetime
from mysql.connector import Error
from mysql.connector import (connection)

#--- MAIN WINDOW -------------------------------------------------------------------------------------------------
# Define Classes
class ShoppingCartSystem(Tk):
    # Initialize User Variables
    user_id = None
    user_type = None
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
    def user_authorization(self, type):
        # Remove Login Frame then replace Header Frame 
        self.frame_sub.destroy()
        self.frame_main.destroy()
        # Set user values
        if type == 0:
            self.user_id = 0 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++ placeholder (pre-login system) 
            self.user_type = "administrator"
        elif type == 1:
            self.user_id = 1 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++ placeholder (pre-login system) 
            self.user_type = "customer"
        self.frame_main = frame_header(self)
        self.frame_main.pack()
        # Load user home frame
        if type == 0:
            self.frame_sub = frame_admin_home(self)
        elif type == 1:
            self.frame_sub = frame_cust_home(self)
        # Add frame to window
        self.frame_sub.pack(fill=BOTH, expand=1)

    # Connect to Database
    def db_connect(self):
        try:
            self.connection = connection.MySQLConnection(
                host="127.0.0.1",
                user="root",
                password="",
                database="dali_9"
            )
            if self.connection.is_connected():
                print("Succesfully connected to database:", self.connection.database)
                self.cursor = self.connection.cursor
        except Error as e:
            print("Error while connecting to MySQL:", e)

    # Disconnect from Database
    def db_disconnect(self):
        if self.connection.is_connected():
            print("Succesfully disconnected from database:", self.connection.database)
            self.connection.close()

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
        if parent.user_type == "customer":
            self.welcometext = "\"Dali-an niyo umorder...\" "
        elif parent.user_type == "administrator":
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
        self.label_cartcount.place(x=850,y=112)
        # Load Ongoing Order
        for self.row in self.parent.rows_orders:
            # Load unfinished Order
            if (self.row[1] == self.parent.user_id and self.row[4] != True):
                self.parent.row_order = self.row
                print("Retrieved current user Order.")
        # Create New Order if all user's orders are finished or no orders exist in database
        if (self.parent.row_order == None):
            self.cursor = self.parent.connection.cursor()
            self.query = "INSERT INTO orders (id_user, datetime_initiate) VALUES (%s, %s)"
            self.cursor.execute(self.query, (self.parent.user_id, datetime.now()))
            self.parent.connection.commit()
            print("Created new user Order.")

        # ==========================================================================================================================================================================================

    # Grocery Cart Popup Window
    def cart_view(self):
        # Intiialize Cart Summary popup window
        self.cart = Toplevel(self.parent)
        self.cart.grab_set()
        # Set Cart Summary popup window's properties and center position to screen
        self.cart.title("Cart Summary")
        self.cart.iconbitmap(self.parent.path_icon)
        self.cart.resizable(False, False)
        self.window_height = 250
        self.window_width = 750
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
        # placeholder content ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        for i in range(50):
            Label(self.frame, text=f"Item {i+1}").pack(pady=5, padx=10)
    # Mouse Scroll Wheel event
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # Activate/Deactivate mousewheel scrolling when mouse cursor is over/not over the respective widget
    def set_mousewheel(self, widget, command):
        """Activate / deactivate mousewheel scrolling when
        cursor is over / not over the widget respectively."""
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))

#--- USER ACCESS FRAMES --------------------------------------------
# Login Frame
class frame_login(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # User Login/Registration
        self.temp_cust = Button(self, text = "Customer", font=("Tahoma", 30, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(1))
        self.temp_cust.pack(pady=60)
        self.temp_mana = Button(self, text = "Administrator", font=("Tahoma", 30, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(0))
        self.temp_mana.pack(pady=20)

# Registration Frame
# placeholder

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
        parent.db_connect()
        self.cursor = parent.connection.cursor()
        # Access Database: Retrieve "inventory" table rows data
        self.cursor.execute("SELECT * FROM inventory")
        parent.rows_items = self.cursor.fetchall()
        print(f"Retrieved {len(parent.rows_items)} rows from \"inventory\" table.")
        # Access Database: Retrieve "orders" table rows data
        self.cursor.execute("SELECT * FROM orders")
        parent.rows_orders = self.cursor.fetchall()
        print(f"Retrieved {len(parent.rows_orders)} rows from \"orders\" table.")
        # Initiate Cart Button
        parent.frame_main.initiatecart()
        # Close Database Connection
        parent.db_disconnect()
        # Initialize grocery inventory rows header titles
        Label(self.frame, text="IMAGE", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=0, pady=10, padx=0)
        Label(self.frame, text="NAME", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=1, pady=10, padx=0)
        Label(self.frame, text="QUANTITY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=2, pady=10, padx=0)
        Label(self.frame, text="PRICE", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=3, pady=10, padx=0)
        Label(self.frame, text="CATEGORY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=4, pady=10, padx=0)
        Label(self.frame, text="").grid(row=0, column=5, pady=10, padx=10)
        Label(self.frame, text="").grid(row=0, column=6, pady=10, padx=10)
        Label(self.frame, text="ORDERED", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=7, pady=10, padx=0)
        # Display retrieved "inventory" table rows
        self.rowcounter = 0
        self.item_image = PhotoImage(file=parent.resource_path("resources/placeholder.png")) #PLACEHOLDER IMAGE--------------------------------------+++++++++++++++++++++++++++++++
        for self.row in parent.rows_items:
            self.rowcounter += 1
            if self.row[5] == "":
                x=1#
            else:
                self.item_image = PhotoImage(file=parent.resource_path(self.row[5]))
            Label(self.frame, image=self.item_image).grid(row=self.rowcounter, column=0, padx=5) #PLACEHOLDER IMAGE-------+++++++++++++++++++++++++++++++
            Label(self.frame, text=self.row[1], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=1, pady=0, padx=0)
            Label(self.frame, text=self.row[2], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=2, pady=0, padx=0)
            Label(self.frame, text=f"Php {self.row[3]}", font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=3, pady=0, padx=0)
            Label(self.frame, text=self.row[4], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=4, pady=0, padx=23)
            Button(self.frame, text="Order", font=("Tahoma", 12, "bold"), fg="white", bg="green", command=lambda item=self.row[1]: self.test(item)).grid(row=self.rowcounter, column=5, pady=0, padx=0)
            Button(self.frame, text="-", font=("Tahoma", 12, "bold"), fg="white", bg="red", command=lambda item=self.row[1]: self.test(item)).grid(row=self.rowcounter, column=6, pady=0, padx=5)
            Label(self.frame, text="- - -", font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=7, pady=0, padx=0)
    # Mouse Scroll Wheel event
    def on_mousewheel(self, event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # Activate/Deactivate mousewheel scrolling when mouse cursor is over/not over the respective widget
    def set_mousewheel(self, widget, command):
        """Activate / deactivate mousewheel scrolling when
        cursor is over / not over the widget respectively."""
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))
    # placeholder +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test(self, item):
        print(item, "Added to cart.")

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