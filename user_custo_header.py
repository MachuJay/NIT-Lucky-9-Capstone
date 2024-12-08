#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
from tkinter import *
from decimal import Decimal
from datetime import datetime

# Dali 9 Brand Conventional Header Frame (Customer)
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
        # Load active user order
        for self.row in self.parent.rows_orders:
            # Load unfinished Order
            if (self.row[1] == self.parent.user_id and self.row[4] != True):
                self.parent.row_order = self.row
                print(f"    Retrieved order number \'{self.parent.row_order[0]}\' for user \'{self.parent.user_id}\'.")
        # Create new order if all user's orders are finished or no orders exist in database
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
                        # If item quantity > 1, subtotal price (price * quantity)
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
        self.cash = 10
        while self.cash < self.parent.row_order[5]:
            self.cash *= 10
        self.text70 = "Amount Due:\nCash:"
        self.text71 = f"{self.parent.row_order[5]}\n{self.cash}.00"
        self.text80 = "--------------"
        self.text90 = "CHANGE:"
        self.text91 = f"{self.cash-self.parent.row_order[5]}"
        self.text100 = ("\n"
            "VATABLE SALES\n"
            "Total Sales\n"
            "VAT AMOUNT (12%)"
        )
        self.text101 = "\n:\n:\n:"
        self.tax = round(self.parent.row_order[5]*Decimal(0.12), 2)
        self.text102 = ("\n"
            f"{self.parent.row_order[5]-self.tax}\n"
            f"{self.parent.row_order[5]-self.tax}\n"
            f"{self.tax}"
        )
        self.text110 = "Total Amount\n\n" #placeholder ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ CHECKOUT BUTTON
        self.text111 = ":\n\n"
        self.text112 = f"{self.parent.row_order[5]}\n\n" #placeholder
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
        # Section 8 (Amount Due and Cashk
        Label(self.frame, text=self.text70, font=(self.fontstyle, self.fontsize, ""), justify=RIGHT, fg="black").grid(row=8, column=0, sticky=E, columnspan=2)
        Label(self.frame, text=self.text71, font=(self.fontstyle, self.fontsize, ""), justify=RIGHT, fg="black").grid(row=8, column=2, sticky=E, columnspan=2)
        # Section 9 (Subdivider)
        Label(self.frame, text=self.text80, font=(self.fontstyle, self.fontsize, ""), fg="black").grid(row=9, column=0, stick=E, columnspan=self.maxcolumns)
        # Section 10 (Change)
        Label(self.frame, text=self.text90, font=(self.fontstyle, self.fontsize, ""), justify=RIGHT, fg="black").grid(row=10, column=0, sticky=E, columnspan=2)
        Label(self.frame, text=self.text91, font=(self.fontstyle, self.fontsize, ""), justify=RIGHT, fg="black").grid(row=10, column=2, sticky=E, columnspan=2)
        # Section 11 (VAT)
        Label(self.frame, text=self.text100, font=(self.fontstyle, self.fontsize, ""), justify=LEFT, fg="black").grid(row=11, column=0, sticky=W)
        Label(self.frame, text=self.text101, font=(self.fontstyle, self.fontsize, ""), justify=LEFT, fg="black").grid(row=11, column=1, sticky=W)
        Label(self.frame, text=self.text102, font=(self.fontstyle, self.fontsize, ""), justify=RIGHT, fg="black").grid(row=11, column=2, sticky=W, columnspan=2)
        # Section 12 (Total)
        Label(self.frame, text=self.text110, font=(self.fontstyle, self.fontsize, "bold"), justify=LEFT, fg="black").grid(row=12, column=0, sticky=W)
        Label(self.frame, text=self.text111, font=(self.fontstyle, self.fontsize, "bold"), justify=LEFT, fg="black").grid(row=12, column=1, sticky=W)
        Label(self.frame, text=self.text112, font=(self.fontstyle, self.fontsize, "bold"), justify=RIGHT, fg="black").grid(row=12, column=2, sticky=W, columnspan=2)
        self.parent.update_orderitems()
    # Mouse Scroll Wheel event
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # Activate/Deactivate mousewheel scrolling when mouse cursor is over/not over the respective widget
    def set_mousewheel(self, widget, command):
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))