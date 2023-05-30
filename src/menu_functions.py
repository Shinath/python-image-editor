from tkinter import *
from view import *
from file_functions import *
from edit_functions import *
from show_functions import *
from process_functions import *
from speedrun import *

class GUI:
  def __init__(self, view):
    self.view = view
    self.ff = FileFunctions(view)
    self.sf = ShowFunctions(view)
    self.ef = EditFunctions(view)
    self.pf = ProcessFunctions(view)
    self.sp = Speedrun(view)
    self.menu_dict = {
        "File":{ 
                  "load" : self.ff.load_image, 
                  "save" : self.ff.save, 
                  "save as..." : self.ff.save_as }, 
        "Edit":{ 
                  "to gray" : self.ef.convert_to_gray , 
                  "split channels" : self.sf.split_channels},
        "Analyze":{ 
                  "histograms" : {
                          "show histogram" : self.sf.show_bar_hist,
                          "contrast stretching" : self.pf.stretch_hist,
                          "equalization" : self.pf.equalization, 
                          "selective stretching" : self.pf.create_selective_stretching_window,}, 
                  "calculate" : {
                          "moments" : self.sp.create_moments_table,
                          "objects" : self.sp.create_object_feature_vector_table,},
                  "watershed" : self.sp.watershed,
                  "skeletonization" : self.sp.skeletonization,
                  "morphological_operations" : self.sp.create_morphological_operations_window,
                  "Hough" : self.sp.detect_lines_hough},

        "Process":{
                  "median filter" : self.sp.create_median_filter_window,
                  "arithmetic operations" : {
                          "negation" : self.pf.negation, 
                          "posterize" : self.pf.posterize,
                          "addition" : lambda: self.sp.create_logic_operation_window(self.sp.addition), 
                          "subtraction" : lambda: self.sp.create_logic_operation_window(self.sp.subtraction),
                          "blending" : self.sp.creating_blending_window,
                          "bitwise" : {
                              "bitwise and" : lambda: self.sp.create_logic_operation_window(self.sp.bitwise_and),
                              "bitwise or" : lambda: self.sp.create_logic_operation_window(self.sp.bitwise_or),
                              "bitwise xor" : lambda: self.sp.create_logic_operation_window(self.sp.bitwise_xor),
                          },
                  },
                  "block operations" : {
                          "blur" : self.sp.create_blur_window,
                          "laplacian" : self.sp.create_laplacian_window, 
                          "canny" : self.sp.create_canny_window,
                          "sobel" : self.sp.create_sobel_window,
                          "linear sharpening" : self.sp.create_linear_sharpening_window, 
                          "edge detection" : self.sp.create_edge_detection_window,},
                  
                  "thresholding" : {
                          "create_thresholding_window" : self.sp.create_thresholding_window,
                          "adaptive thresholding" : self.sp.create_adaptive_thresholging_window,
                          "otsu's thresholding" : self.sp.otsus_thresholding},
                  },

        "info" : self.ff.info_window
        }

  def generate_menubuttons(self):
    for menu in self.menu_dict:
      mb = Menubutton(master = self.view, text = menu, indicatoron=False, font=("Helvetica", 17))
      if not isinstance(self.menu_dict[menu], dict):
        mb.bind("<Button-1>", self.menu_dict[menu])
      else:
        mb.menu = Menu(mb)
        mb["menu"] = mb.menu
        for function_label in self.menu_dict[menu]:
          if isinstance(self.menu_dict[menu][function_label], dict):
            submenu = Menu(mb.menu)
            for label in self.menu_dict[menu][function_label]:
              if isinstance(self.menu_dict[menu][function_label][label], dict):
                submenu2 = Menu(submenu)
                for sublabel in self.menu_dict[menu][function_label][label]:
                  submenu2.add_command(label= sublabel, command= self.menu_dict[menu][function_label][label][sublabel])
                submenu.add_cascade(label=label, menu=submenu2)
              else:
                submenu.add_command(label= label, command= self.menu_dict[menu][function_label][label])
            mb.menu.add_cascade(label=function_label, menu=submenu)
          else:
            mb.menu.add_command(label=function_label, command= self.menu_dict[menu][function_label])
      mb.pack(side= LEFT)