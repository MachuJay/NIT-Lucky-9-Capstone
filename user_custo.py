#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
import tkinter as tk
from mysql.connector import Error

# Customer Frame: Home
class frame_cust_home(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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
        # Access Database: Retrieve "orders" table rows data
        self.cursor.execute("SELECT * FROM orders")
        parent.rows_orders = self.cursor.fetchall()
        print(f"    Retrieved \'{len(parent.rows_orders)}\' rows from \"orders\" table.")
        # Initiate Cart Button
        parent.frame_main.initiatecart()
        # Close Database Connection
        parent.db_disconnect("announce")
        # Initialize Grocery inventory rows header titles
        tk.Label(self.frame, text="IMAGE", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=0, pady=10, padx=0)
        tk.Label(self.frame, text="NAME", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=1, pady=10, padx=0)
        tk.Label(self.frame, text="QUANTITY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=2, pady=10, padx=0)
        tk.Label(self.frame, text="PRICE", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=3, pady=10, padx=0)
        tk.Label(self.frame, text="CATEGORY", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=4, pady=10, padx=0)
        tk.Label(self.frame, text="").grid(row=0, column=5, pady=10, padx=10)
        tk.Label(self.frame, text="").grid(row=0, column=6, pady=10, padx=10)
        tk.Label(self.frame, text="ORDERED", font=("Segoe UI", 10, "bold"), fg="white", bg="black").grid(row=0, column=7, pady=10, padx=0)
        # Display retrieved "inventory" table rows
        self.item_placeholder = tk.PhotoImage(file=parent.resource_path("resources/placeholder.png"))
        self.rowcounter = 0
        for self.row in parent.rows_items:
            self.rowcounter += 1
            # If 'imagepath' value is empty
            if self.row[5] == "":
                self.item_image = self.item_placeholder
            else:
                self.item_image = tk.PhotoImage(file=parent.resource_path(self.row[5]))
                parent.orderlist_images.append(self.item_image)
            # image
            self.label_image = tk.Label(self.frame, image=self.item_image)
            self.label_image.grid(row=self.rowcounter, column=0, padx=5)
            # name
            tk.Label(self.frame, text=self.row[1], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=1, pady=0, padx=0)
            # quantity
            tk.Label(self.frame, text=self.row[2], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=2, pady=0, padx=0)
            # price
            tk.Label(self.frame, text=f"Php {self.row[3]}", font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=3, pady=0, padx=0)
            # category
            tk.Label(self.frame, text=self.row[4], font=("Tahoma", 16, "")).grid(row=self.rowcounter, column=4, pady=0, padx=23)
            # order buttons
            tk.Button(self.frame, text="Order", font=("Tahoma", 12, "bold"), fg="white", bg="green", command=lambda item=self.row[0]: self.item_add(item)).grid(row=self.rowcounter, column=5, pady=0, padx=0)
            tk.Button(self.frame, text="-", font=("Tahoma", 12, "bold"), fg="white", bg="red", command=lambda item=self.row[0]: self.item_remove(item)).grid(row=self.rowcounter, column=6, pady=0, padx=5)
            # order counter labels
            self.label_counter = tk.Label(self.frame, text="- - -", font=("Tahoma", 16, ""))
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