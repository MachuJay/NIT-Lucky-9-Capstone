#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
import tkinter as tk
from mysql.connector import Error

# Administrator Frame: Home
class frame_admin_home(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Inventory List View
        self.canvastime(parent)

        # Other admin tasks
        #placeholder

    # Inventory List View
    def canvastime(self, parent):
        # Initialize Canvas
        self.canvas = tk.Canvas(parent)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # Initialize Scrollbar
        self.scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Configure Canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        # Initialize internal Frame into an internal Window within the Canvas
        self.frame = tk.Frame(self.canvas)
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
        # Close Database Connection
        parent.db_disconnect("announce")
        # Initialize Grocery inventory rows header titles
        tk.Label(self.frame, text="NAME", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=0, pady=10, padx=0)
        tk.Label(self.frame, text="QUANTITY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=1, pady=10, padx=0)
        tk.Label(self.frame, text="PRICE", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=2, pady=10, padx=0)
        tk.Label(self.frame, text="").grid(row=0, column=3, pady=10, padx=10)
        tk.Label(self.frame, text="CATEGORY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=4, pady=10, padx=0)
        # Display retrieved "inventory" table rows
        self.rowcounter = 0
        for self.row in parent.rows_items:
            self.rowcounter += 1
            # name
            tk.Label(self.frame, text=self.row[1], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=0, pady=0, padx=0)
            # quantity
            tk.Label(self.frame, text=self.row[2], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=1, pady=0, padx=0)
            # price
            self.label_price = tk.Label(self.frame, text=f"Php {self.row[3]}", font=("Tahoma", 16, ""))
            self.label_price.grid(row=self.rowcounter, column=2, pady=0, padx=0)
            parent.adminlist_prices[self.rowcounter-1] = self.label_price
            # adjust price buttons
            self.fg = ""
            self.bg = ""
            if self.rowcounter % 2 == 0:
                self.fg = "black"
                self.bg = "white"
            else:
                self.fg = "white"
                self.bg = "black"
            tk.Button(self.frame, text="Adjust Price", font=("Tahoma", 12, "bold"), fg=self.fg, bg=self.bg, command=lambda id=self.row[0]: self.adjustprice(id)).grid(row=self.rowcounter, column=3, pady=0, padx=0)
            # category
            tk.Label(self.frame, text=self.row[4], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=4, pady=0, padx=23)
    # Mouse Scroll Wheel event
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # Activate/Deactivate mousewheel scrolling when mouse cursor is over/not over the respective widget
    def set_mousewheel(self, widget, command):
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))
    def adjustprice(self, id):
        # Intiialize Cart Summary popup window
        self.cart = tk.Toplevel(self.parent)
        self.cart.focus_set()
        self.cart.grab_set()
        # Set Cart Summary popup window's properties and center position to screen
        self.cart.title("Pricing")
        self.cart.iconbitmap(self.parent.path_icon)
        self.cart.resizable(False, False)
        self.window_height = 230
        self.window_width = 380
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/2))
        self.cart.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))
        # User input to change item price
        self.row_adjust = None
        for self.row_item in self.parent.rows_items:
            if (self.row_item[0] == id):
                self.row_adjust = self.row_item
        tk.Label(self.cart, text="-----------ADJUST ITEM PRICE-----------", font=("Segoe UI", 16, "bold"), fg="white", bg="black").grid(row=0, column=0, pady=0, padx=0, columnspan=2)
        tk.Label(self.cart, text="NAME", font=("Segoe UI", 16, "bold"), fg="white", bg="#A21F6A").grid(row=1, column=0, pady=3, padx=0, sticky=tk.W)
        tk.Label(self.cart, text=self.row_adjust[1], font=("Segoe UI", 18, "bold"), fg="black").grid(row=1, column=1, pady=3, padx=0, sticky=tk.W)
        tk.Label(self.cart, text="PRICE", font=("Segoe UI", 16, "bold"), fg="white", bg="#A21F6A").grid(row=2, column=0, pady=3, padx=0, sticky=tk.W)
        tk.Label(self.cart, text=f"Php {self.row_adjust[3]}", font=("Segoe UI", 16, "bold"), fg="black").grid(row=2, column=1, pady=3, padx=0, sticky=tk.W)
        tk.Label(self.cart, text="New Price:", font=("Segoe UI", 16, "bold"), fg="black").grid(row=3, column=0, pady=3, padx=0, sticky=tk.W)
        self.input_price = tk.Entry(self.cart, font=("Segoe UI", 16, "bold"), fg="black", width=18)
        self.input_price.grid(row=3, column=1, pady=3, padx=0, sticky=tk.W)
        # confirm button
        tk.Button(self.cart, text="CONFIRM", font=("Tahoma", 16, ""), fg="#A21F6A", bg="black", command=lambda id=id, name=self.row_adjust[1], entryfield=self.input_price: self.price_update(id, name, entryfield)).grid(row=4, column=0, pady=8, padx=0, columnspan=2)
    def price_update(self, id, name, entryfield):
        self.price = entryfield.get()
        # Check if input is valid
        try:
            # Convert string to float
            self.price = float(self.price)
            # Convert float to string with 2 decimal places
            self.price = f"{self.price:.2f}"
            # Convert string to float then round up float value to 2 decimal places
            self.price = round(float(self.price), 2)
            # Database Access: Update inventory item's price column
            self.parent.db_connect("announce")
            self.cursor = self.parent.connection.cursor()
            self.cursor.execute(f"UPDATE inventory SET price = {self.price} WHERE id_item = {id}")
            print(f"    Updating price of \'{name}\' from \'{self.row_adjust[3]}\' to \'{self.price}\'...")
            self.parent.connection.commit()
            print(f"    Succesfully updated price to \'{self.price}\'")
            # Query updated price's database value
            self.cursor = self.parent.connection.cursor()
            self.cursor.execute(f"SELECT * FROM inventory WHERE id_item = {id}")
            self.row_item = self.cursor.fetchone()
            self.parent.db_disconnect("announce")
            # Update Price label's value
            self.rowcounter = 0
            # Traverse inventory items list
            for self.row in self.parent.rows_items:
                # If current row is equal to recently modified item's price row, update label's text value
                if (self.row[0] == id):
                    self.parent.adminlist_prices[self.rowcounter].config(text=f"Php {self.row_item[3]}")
                self.rowcounter += 1
            # Exit popup window
            self.cart.destroy()
        except Error as e:
            print("Error while connecting to MySQL:", e)
        except:
            print("    Invalid Input.")