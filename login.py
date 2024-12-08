#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Import packages
from tkinter import *

#--- USER ACCESS FRAMES --------------------------------------------
# Login Frame
class frame_login(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # User Login/Registration
        self.temp_cust = Button(self, text = "Customer", font=("Tahoma", 30, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(1)) #pass user id in param
        self.temp_cust.pack(pady=60)
        self.temp_mana = Button(self, text = "Administrator", font=("Tahoma", 30, "bold"), fg="white", bg="black", command=lambda: parent.user_authorization(0)) #pass user id in param
        self.temp_mana.pack(pady=20)
        # verify user's username and password then pass value to user_authorization()
        #placeholder

# Registration Frame
# placeholder
# exit program to "return" to login frame