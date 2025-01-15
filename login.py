#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
import tkinter as tk

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
        self.label_title = tk.Label(self, text = "User Login", font=(self.fontstyle, self.fontsize, "bold"), fg="black", justify="center")
        self.label_title.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        # Username Row
        self.label_username = tk.Label(self, text = "Username:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", anchor="w")
        self.label_username.grid(row=1, column=0, sticky=tk.NSEW)
        self.text_username = tk.Entry(self, font=(self.fontstyle, self.fontsize))
        self.text_username.grid(row=1, column=1)
        # Password Row
        self.label_password = tk.Label(self, text = "Password:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", anchor="w")
        self.label_password.grid(row=2, column=0, sticky=tk.NSEW)
        self.text_password = tk.Entry(self, font=(self.fontstyle, self.fontsize), show="*")
        self.text_password.grid(row=2, column=1)
        # Submit Button
        self.button_login = tk.Button(self, text = "Login", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", command=lambda: self.login())
        self.button_login.grid(row=3, column=0, columnspan=2)
        # Padding
        self.label_spacer = tk.Label(self, text = "", font=(self.fontstyle, self.fontsize, "bold"))
        self.label_spacer.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
        # Switch to Registration Interface Button
        self.button_registerload = tk.Button(self, text = "Register", font=(self.fontstyle, self.fontsize, "bold"), fg="black", bg="white", command=lambda: self.registerload())
        self.button_registerload.grid(row=5, column=1, pady=0, sticky=tk.E)

    # Switch to User Registration Interface
    def registerload(self):
        # Remove Login tkinter Widgets then Initialize Registration Widgets
        self.label_username.destroy()
        self.text_username.destroy()
        self.label_password.destroy()
        self.text_password.destroy()
        self.button_login.destroy()
        self.label_spacer.destroy()
        self.button_registerload.destroy()
        # Title Label
        self.label_title.config(text = "User Registration")
        # Username Row
        self.label_username = tk.Label(self, text = "Username:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", anchor="w")
        self.label_username.grid(row=1, column=0, sticky=tk.NSEW)
        self.text_username = tk.Entry(self, font=(self.fontstyle, self.fontsize))
        self.text_username.grid(row=1, column=1)
        # Password Row
        self.label_password = tk.Label(self, text = "Password:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", anchor="w")
        self.label_password.grid(row=2, column=0, sticky=tk.NSEW)
        self.text_password = tk.Entry(self, font=(self.fontstyle, self.fontsize), show="*")
        self.text_password.grid(row=2, column=1)
        # Nickname Row
        self.label_nickname = tk.Label(self, text = "Nickname:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", anchor="w")
        self.label_nickname.grid(row=3, column=0, sticky=tk.NSEW)
        self.text_nickname = tk.Entry(self, font=(self.fontstyle, self.fontsize))
        self.text_nickname.grid(row=3, column=1)
        # Submit Button
        self.button_register = tk.Button(self, text = "Register", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", command=lambda: self.register())
        self.button_register.grid(row=4, column=0, columnspan=2)
        # Padding
        self.label_spacer = tk.Label(self, text = "", font=(self.fontstyle, 5, "italic"))
        self.label_spacer.grid(row=5, column=0, columnspan=2)
        # "Switch" to Login Interface Button (Restart Program)
        self.button_loginload = tk.Button(self, text = "Return to Login", font=(self.fontstyle, self.fontsize, "bold"), fg="black", bg="white", command=lambda: self.parent.logout())
        self.button_loginload.grid(row=6, column=1, pady=0, sticky=tk.E)

    # Login Button Functionality
    def login(self):
        #---------------Add Code In-between Here ----------------------------------------------------------------------------------
        # (optional) Get user input and store into variables
        #>

        # Access Database: Retrieve row 
        self.parent.db_connect()
        self.cursor = self.parent.connection.cursor()
        #>---Perform MySQL connection query in this line---<
        self.row_user = self.cursor.fetchone() # Store retrieved database row into tuple type variable "self.row_user"
        self.parent.db_disconnect()

        # Login user if fetched row is not empty
        #>
        
        #------------------------------- To Here ----------------------------------------------------------------------------------
        ''' NOTES:
            Function to get user input Username: self.text_username.get()
            Function to get user input Password: self.text_password.get()
            Sample MySQL connection query: self.cursor.execute(f"SELECT * FROM users WHERE id = {id}")
            self.row_user[0] = "id" column of "users" table
            self.row_user[1] = "username" column of "users" table
            self.row_user[2] = "password" column of "users" table
            self.row_user[4] = "name" column of "users" table
        '''
        # Force login specific user
        #self.parent.user_authorization(0) #Admin
        #self.parent.user_authorization(1) #Customer

    # Register Button Functionality
    def register(self):
        #---------------Add Code In-between Here ----------------------------------------------------------------------------------
        # (optional) Get user input and store into variables
        #>

        #>Add if-condition to only access database if all fields are not empty (the code following code block below):
        # Access Database: Insert new table row for new user
        self.parent.db_connect()
        self.cursor = self.parent.connection.cursor()
        #>---Perform MySQL connection query in this line---<
        self.parent.db_disconnect()

        # Return to Login interface (Restart Program)
        self.parent.logout()

        #------------------------------- To Here ----------------------------------------------------------------------------------
        ''' NOTES:
            Function to get user input Username: self.text_username.get()
            Function to get user input Password: self.text_password.get()
            Function to get user input Nickname: self.text_nickname.get()
            Sample MySQL connection query: self.cursor.execute(f"INSERT INTO orders (id_user, datetime_initiate) VALUES ({id}, {date})")
            self.row_user[1] = "username" column of "users" table
            self.row_user[2] = "password" column of "users" table
            self.row_user[4] = "name" column of "users" table
        '''