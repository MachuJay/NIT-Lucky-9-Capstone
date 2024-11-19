# Import packages
from tkinter import *
import os, sys

# Define Classes
class App(Tk):
    def __init__(self):
        super().__init__()

        #Initialize resources items paths
        self.path_icon = self.resource_path("resources/puregro.ico")
        self.path_banner = self.resource_path("resources/banner_puregro.png")

        # Initialize window properties
        self.title("Puregro Virtual Shopping Cart")
        self.iconbitmap(self.path_icon)
        self.resizable(False, False)

        # Center program window on screen
        self.window_height = 450
        self.window_width = 700
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/2))
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))

        # Variables
        self.togglestatus = True

        # Brand Intro Banner
        self.image_banner = PhotoImage(file=self.path_banner)
        self.my_labelimage = Label(self, image=self.image_banner)
        self.my_labelimage.pack(pady=20)
        
        # Label Box
        self.my_label = Label(self, text="Hello Lucky 9!", font=("Helvetica", 42))
        self.my_label.pack(pady=20)

        # Toggle Button
        self.my_button = Button(self, text = "Toggle", command=self.change)
        self.my_button.pack(pady=20)

    # Get the absolute path to a resource file (Works in dev and built modes)
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            # Running as an executable
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Toggle Button Action
    def change(self):
        if self.togglestatus == True:
            self.my_label.config(text="GUI App Initialized.")
            self.togglestatus = False
        else:
            self.my_label.config(text="Hello Lucky 9!")
            self.togglestatus = True

# Define and Instantiate Shopping Cart App 
app = App()
app.mainloop()