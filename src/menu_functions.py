from tkinter import *
from view import *
from file_functions import *
from edit_functions import *
from show_functions import *
from process_functions import *

def generate_menubuttons(view):
    ff = FileFunctions(view)
    sf = ShowFunctions(view)
    ef = EditFunctions(view)
    pf = ProcessFunctions(view)
    
    menu_dict = {
      "file" : { "load" : ff.load_image, "save" : ff.save, "save as..." : ff.save_as }, 
      "edit" : { "to gray" : ef.convert_to_gray },
      "show" : { "histogram" : sf.show_bar_hist },
      "process" : { "split channels" : sf.split_channels, "contrast stretching" : pf.stretch_hist, "equalization" : pf.equalization,
                    "negation" : pf.negation, "posterize" : pf.posterize},
      "info" : ff.info_window,
      }
    for menu in menu_dict:
      if not isinstance(menu_dict[menu], dict):
        mb = Menubutton(master = view, text = menu, indicatoron=False, font=("Helvetica", 17))
        mb.bind("<Button-1>", menu_dict[menu])
      elif not menu_dict[menu]:
        mb = Menubutton(master = view, text = menu, indicatoron=False, font=("Helvetica", 17))
      else:
        mb = Menubutton(view, text=menu, indicatoron=False, font=("Helvetica", 17))
        mb.menu = Menu(mb)
        mb["menu"] = mb.menu
        for function_labels in menu_dict[menu]:
          mb.menu.add_command(label=function_labels, command = menu_dict[menu][function_labels])
      mb.pack(side = LEFT)