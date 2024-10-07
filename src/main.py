from tkinter import *
from view import *
from image import *
from menu_functions import *
import json


menu = View()
menu.bind('<Escape>', lambda: menu.destroy())
style = ttk.Style("darkly")
gui = GUI(menu)
gui.generate_menubuttons()
menu.mainloop()