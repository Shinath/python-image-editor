from tkinter import *
from view import *
from file_functions import *
from edit_functions import *
from show_functions import *
from process_functions import *
from speedrun import *

def generate_menubuttons(view):
    ff = FileFunctions(view)
    sf = ShowFunctions(view)
    ef = EditFunctions(view)
    pf = ProcessFunctions(view)
    sp = Speedrun(view)
  
    menu_dict = {
      "file" : { "load" : ff.load_image, "save" : ff.save, "save as..." : ff.save_as }, 
      "edit" : { "to gray" : ef.convert_to_gray },
      "show" : { "histogram" : sf.show_bar_hist },
      "process" : { "split channels" : sf.split_channels, "contrast stretching" : pf.stretch_hist, "equalization" : pf.equalization,
                    "negation" : pf.negation, "posterize" : pf.posterize},
      "speedrun" : {"selective stretching" : pf.create_selective_stretching_window, "blur" : sp.create_blur_window,
                    "laplacian" : sp.create_laplacian_window, "canny" : sp.create_canny_window,
                    "linear sharpening" : sp.create_linear_sharpening_window, "edge detection" : sp.create_edge_detection_window,
                    "addition" : lambda: sp.create_logic_operation_window(sp.addition), 
                    "subtraction" : lambda: sp.create_logic_operation_window(sp.subtraction),
                    "blending" : sp.creating_blending_window,
                    "bitwise and" : lambda: sp.create_logic_operation_window(sp.bitwise_and),
                    "bitwise or" : lambda: sp.create_logic_operation_window(sp.bitwise_or),
                    "bitwise xor" : lambda: sp.create_logic_operation_window(sp.bitwise_xor),},
      "info" : ff.info_window
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
        for function_label in menu_dict[menu]:
          mb.menu.add_command(label=function_label, command = menu_dict[menu][function_label])
      mb.pack(side = LEFT)