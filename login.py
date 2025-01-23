#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
import tkinter as tk
import hashlib

#--- USER ACCESS FRAMES --------------------------------------------
# Login Frame
class frame_login(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Initialize Canvas
        self.fontsize = 30
        self.fontstyle = "Tahoma"
        # Title Label
        self.label_title = tk.Label(self, text = "User Login", font=(self.fontstyle, self.fontsize, "bold"), fg="#322d31", justify="center")
        self.label_title.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        # Username Row
        self.label_username = tk.Label(self, text = "Username:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="#525e75", anchor="w")
        self.label_username.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.text_username = tk.Entry(self, font=(self.fontstyle, self.fontsize))
        self.text_username.grid(row=1, column=2)
        # Password Row
        self.label_password = tk.Label(self, text = "Password:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="#525e75", anchor="w")
        self.label_password.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)
        self.text_password = tk.Entry(self, font=(self.fontstyle, self.fontsize), show="*")
        self.text_password.grid(row=2, column=2)
        # Submit Button
        self.button_login = tk.Button(self, text = "Login", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="#525e75", command=lambda: self.login())
        self.button_login.grid(row=3, column=0, columnspan=3)
        # Padding
        self.label_spacer = tk.Label(self, text = "", font=(self.fontstyle, self.fontsize, "bold"))
        self.label_spacer.grid(row=4, column=0, columnspan=3)
        # Context Message Label
        self.label_notif = tk.Label(self, text = "", font=(self.fontstyle, self.fontsize, "bold"), fg="black", justify="left")
        self.label_notif.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        # Switch to Registration Interface Button
        self.button_registerload = tk.Button(self, text = "Register", font=(self.fontstyle, self.fontsize, "bold"), fg="#322d31", bg="white", command=lambda: self.registerload())
        self.button_registerload.grid(row=5, column=2, pady=0, sticky=tk.E)

    # Switch to User Registration Interface
    def registerload(self):
        # Remove Login tkinter Widgets then Initialize Registration Widgets
        self.label_username.destroy()
        self.text_username.destroy()
        self.label_password.destroy()
        self.text_password.destroy()
        self.button_login.destroy()
        self.label_spacer.destroy()
        self.label_notif.destroy()
        self.button_registerload.destroy()
        # Title Label
        self.label_title.config(text = "User Registration")
        # Username Row
        self.label_username = tk.Label(self, text = "Username:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="#78938a", anchor="w")
        self.label_username.grid(row=1, column=0, sticky=tk.NSEW)
        self.text_username = tk.Entry(self, font=(self.fontstyle, self.fontsize))
        self.text_username.grid(row=1, column=1)
        # Password Row
        self.label_password = tk.Label(self, text = "Password:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="#78938a", anchor="w")
        self.label_password.grid(row=2, column=0, sticky=tk.NSEW)
        self.text_password = tk.Entry(self, font=(self.fontstyle, self.fontsize), show="*")
        self.text_password.grid(row=2, column=1)
        # Nickname Row
        self.label_nickname = tk.Label(self, text = "Nickname:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="#78938a", anchor="w")
        self.label_nickname.grid(row=3, column=0, sticky=tk.NSEW)
        self.text_nickname = tk.Entry(self, font=(self.fontstyle, self.fontsize))
        self.text_nickname.grid(row=3, column=1)
        # Submit Button
        self.button_register = tk.Button(self, text = "Register", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="#78938a", command=lambda: self.register())
        self.button_register.grid(row=4, column=0, columnspan=2)
        # Padding
        self.label_spacer = tk.Label(self, text = "", font=(self.fontstyle, 5, "italic"))
        self.label_spacer.grid(row=5, column=0, columnspan=2)
        # Context Message Label
        self.label_notif = tk.Label(self, text = "", font=(self.fontstyle, self.fontsize, "bold"), fg="black", justify="left")
        self.label_notif.grid(row=6, column=0, columnspan=2, sticky=tk.W)
        # "Switch" to Login Interface Button (Restart Program)
        self.button_loginload = tk.Button(self, text = "Back to Login", font=(self.fontstyle, self.fontsize, "bold"), fg="#322d31", bg="white", command=lambda: self.parent.logout())
        self.button_loginload.grid(row=6, column=1, pady=0, sticky=tk.E)

    # Login Button Functionality
    def login(self):
        # Check if user input fields are not empty
        if self.text_username.get() != "" and self.text_password.get() != "":
            # Access Database: Query if user input matches "users" table row
            self.parent.db_connect()
            self.cursor = self.parent.connection.cursor()
            self.hashedpassword = hashlib.md5(self.text_password.get().encode()).hexdigest()
            self.cursor.execute(f"SELECT id FROM users WHERE username = '{self.text_username.get()}' and password = '{self.hashedpassword}'")
            self.query_userid = self.cursor.fetchone()
            self.parent.db_disconnect()
            # Login user using retrieved user id if table row exists
            if self.query_userid != None:
                self.parent.user_authorization(self.query_userid[0])
            else:
                self.label_notif.config(text = "User does not exist.")
        else:
            if self.text_username.get() != "":
                self.label_notif.config(text = "Password field empty.")
            elif self.text_password.get() != "":
                self.label_notif.config(text = "Username field empty.")
            else:
                self.label_notif.config(text = "Fill up both fields.")

    # Register Button Functionality
    def register(self):
        # Check if user input fields are not empty
        if self.text_username.get() != "" and self.text_password.get() != "" and self.text_nickname.get() != "":
            # Access Database: Check if username already exists
            self.parent.db_connect()
            self.cursor = self.parent.connection.cursor()
            self.cursor.execute(f"SELECT id FROM users WHERE username = '{self.text_username.get()}'")
            self.query_username = self.cursor.fetchone()
            self.parent.db_disconnect()
            # Register user if username is unique
            if self.query_username == None:
                # Access Database: Insert new table row for new user
                self.parent.db_connect()
                self.cursor = self.parent.connection.cursor()
                self.hashedpassword = hashlib.md5(self.text_password.get().encode()).hexdigest()
                self.query = "INSERT INTO users (username, password, type, name) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(self.query, (self.text_username.get(), self.hashedpassword, 1, self.text_nickname.get()))
                self.parent.connection.commit()
                self.parent.db_disconnect()
                # Disable interactable widgets
                self.text_username.config(state = "disabled")
                self.text_password.config(state = "disabled")
                self.text_nickname.config(state = "disabled")
                self.button_register.config(state = "disabled")
                self.label_notif.config(text = "User registered.")
            else:
                self.label_notif.config(text = "Username taken.")
        else:
            self.label_notif.config(text = "Fill up all fields.")