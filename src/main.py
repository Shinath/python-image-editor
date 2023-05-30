from tkinter import *
from view import *
from image import *
from menu_functions import *


menu = View()
gui = GUI(menu)
gui.generate_menubuttons()
menu.mainloop()