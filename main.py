#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
from tkinter import *
import os, sys
from mysql.connector import (connection)
from mysql.connector import Error

#--- MAIN WINDOW -------------------------------------------------------------------------------------------------
# Define Classes
class ShoppingCartSystem(Tk):
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

        # Initialize variables
        self.user_type = None
        self.user_id = None

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
        # remove Login Frame then replace Header Frame 
        self.frame_sub.destroy()
        self.frame_main.destroy()
        self.frame_main = frame_header(self)
        self.frame_main.pack()
        # Load user home frame
        if type == 0:
            self.user_id = 0 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++ placeholder (pre-login system) 
            self.user_type = "administrator"
            self.frame_sub = frame_admin_home(self)
        elif type == 1:
            self.user_id = 1 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++ placeholder (pre-login system) 
            self.user_type = "customer"
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
        
#-----------------------------------------------------------------------------------------------------------------
#--- HEADER FRAMES -----------------------------------------------------------------------------------------------
# Dali 9 Brand Header Frame
class frame_mainheader(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Brand Intro Banner
        self.image_banner = PhotoImage(file=self.parent.path_mainbanner)
        self.label_banner = Label(self, image=self.image_banner)
        self.label_banner.pack()
        self.image_brand = PhotoImage(file=self.parent.path_mainbrand)
        self.label_brand = Label(self, image=self.image_brand)
        self.label_brand.place(x=412,y=0)
        self.label_brand.lift()

# Dali 9 Brand Conventional Header Frame
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
        self.label_brand.place(x=50,y=0)
        self.label_brand.lift()
        self.button_logout = Button(self, text = "LOG OUT", fg="white", bg="red", command=lambda: self.logout())
        self.button_logout.place(x=950,y=2)

    def initiatecart(self):
        self.image_cart = PhotoImage(file=self.parent.path_cart)
        self.button_cart = Button(self, image=self.image_cart, command=lambda: self.cartshit()) #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.button_cart.place(x=800,y=33)
        self.button_cart.lift()
        self.label_cartcount = Label(self, text="(99 items)", fg="white", bg="#A21F6A", justify="center", font=("Tahoma", 16, ""))
        self.label_cartcount.place(x=850,y=112)

    def cartshit(self):
        print("UWOOOOOO SEGGGGS")

    def logout(self):
        print("Logout.")

#--- USER ACCESS FRAMES --------------------------------------------
# Login Frame
class frame_login(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # User Login/Registration
        self.temp_cust = Button(self, text = "Customer", command=lambda: self.parent.user_authorization(1))
        self.temp_cust.pack(pady=60)
        self.temp_mana = Button(self, text = "Administrator", command=lambda: self.parent.user_authorization(0))
        self.temp_mana.pack(pady=20)

    def login(self):
        # placeholder
        print("")

# Registration Frame
#placeholder

#--- CUSTOMER USER FRAMES ------------------------------------------
# Customer Frame: Home
class frame_cust_home(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Initialize Canvas
        self.canvas = Canvas(self.parent)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # mousewheel event to scroll the canvas vertically
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Initialize Scrollbar
        self.scrollbar = Scrollbar(parent, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # Configure Canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        # Bind mouse wheel event
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        # Initialize internal Frame into an internal Window within the Canvas
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        # Access Database: Retrieve "Inventory" table rows data
        self.parent.db_connect()
        self.cursor = self.parent.connection.cursor()
        self.cursor.execute("SELECT * FROM inventory")
        self.rows = self.cursor.fetchall()
        print(f"Succsesfully retrieved {len(self.rows)} rows.")
        # Initiate Order's Cart+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #
        self.parent.frame_main.initiatecart()
        #
        #self.cursor = self.parent.connection.cursor()
        #self.cursor.execute("SELECT * FROM inventory")
        #self.parent.frame_main = frame_mainheader(self.parent)
        self.parent.db_disconnect()
        # Initialize grocery inventory rows header titles
        Label(self.frame, text="Image", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, pady=10, padx=0)
        Label(self.frame, text="Name", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, pady=10, padx=0)
        Label(self.frame, text="Quantity", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, pady=10, padx=0)
        Label(self.frame, text="Price", font=("Segoe UI", 10, "bold")).grid(row=0, column=3, pady=10, padx=0)
        Label(self.frame, text="Category", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, pady=10, padx=0)
        Label(self.frame, text="").grid(row=0, column=5, pady=10, padx=10)
        # Display retrieved "inventory" table rows
        self.rowcounter = 0
        self.test_image = PhotoImage(file="resources/image1.png") #PLACEHOLDER IMAGE--------------------------------------+++++++++++++++++++++++++++++++
        for self.row in self.rows:
            self.rowcounter += 1
            Label(self.frame, image=self.test_image).grid(row=self.rowcounter, column=0, padx=5) #PLACEHOLDER IMAGE-------+++++++++++++++++++++++++++++++
            Label(self.frame, text=self.row[1], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=1, pady=0, padx=0)
            Label(self.frame, text=self.row[2], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=2, pady=0, padx=0)
            Label(self.frame, text=f"Php {self.row[3]}", font=("Tahoma", 16, ""), justify="right").grid(row=self.rowcounter, column=3, pady=0, padx=0)
            Label(self.frame, text=self.row[4], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=4, pady=0, padx=23)
            Button(self.frame, text="Order", command=lambda item=self.row[1]: self.test(item)).grid(row=self.rowcounter, column=5, pady=0, padx=0)

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
        #---trial---
        
#-----------------------------------------------------------------------------------------------------------------
#--- RUNTIME INITIATE --------------------------------------------------------------------------------------------
# Define and Instantiate Shopping Cart App 
ShoppingCartSystem().mainloop()

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------
'''
import hashlib
# Function to hash a password using MD5
def hash_password_md5(password: str) -> str:
    # Encode the password to bytes, then hash it
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed
# Example usage
if __name__ == "__main__":
    # Input password
    plain_password = "my_se33c33ure_password"

    # Hash the password
    hashed_password = hash_password_md5(plain_password)
    print(f"MD5 Hashed password: {hashed_password}")
'''
#-----------------------------------------------------------------------------------------------------------------