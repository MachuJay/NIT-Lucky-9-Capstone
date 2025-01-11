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

        self.label_title = tk.Label(self, text = "User Login", font=(self.fontstyle, self.fontsize, "bold"), fg="black", justify="center")
        self.label_title.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        
        self.label_username = tk.Label(self, text = "Username:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", anchor="w")
        self.label_username.grid(row=1, column=0, sticky=tk.NSEW)
        self.text_username = tk.Entry(self, font=(self.fontstyle, self.fontsize))
        self.text_username.grid(row=1, column=1)

        self.label_password = tk.Label(self, text = "Password:", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", anchor="w")
        self.label_password.grid(row=2, column=0, sticky=tk.NSEW)
        self.text_password = tk.Entry(self, font=(self.fontstyle, self.fontsize), show="*")
        self.text_password.grid(row=2, column=1)

        self.button_login = tk.Button(self, text = "Login", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(1))
        self.button_login.grid(row=3, column=0, columnspan=2)
        
        self.button_registerload = tk.Button(self, text = "Register", font=(self.fontstyle, self.fontsize, "bold"), fg="black", bg="white", command=lambda: self.registerload())
        self.button_registerload.grid(row=4, column=1, pady=0, sticky=tk.E)

        # Switch to User Registration Interface
        def registerload(self):
            print("register time")
        '''
        self.temp_cust = tk.Button(self, text = "Customer", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(1)) #pass user id in param
        self.temp_cust.grid(row=3, column=0, pady=0)
        self.temp_mana = tk.Button(self, text = "Administrator", font=(self.fontstyle, self.fontsize, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(0)) #pass user id in param
        self.temp_mana.grid(row=4, column=0, pady=0)
        '''

        # verify user's username and password
        
        # pass value to user_authorization()
        #parent.user_authorization(userid)


# Registration Frame
# placeholder
# exit program to "return" to login frame