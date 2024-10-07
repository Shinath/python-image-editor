from tkinter import *
from view import *
from file_functions import *
from edit_functions import *
from analyze_functions import *
from process_functions import *
import ttkbootstrap as ttk


class GUI:
  def __init__(self, view):
    self.view = view
    self.ff = FileFunctions(view)
    self.ef = EditFunctions(view)
    self.af = AnalyzeFunctions(view)
    self.sp = ProcessFunctions(view)
    self.menu_dict = {
        "File":{ 
                  "load" : self.ff.load_image, 
                  "save" : self.ff.save, 
                  "save as..." : self.ff.save_as }, 
        "Edit":{ 
                  "to gray" : self.ef.convert_to_gray , 
                  "split channels" : self.ef.split_channels},
        "Analyze":{ 
                  "histograms" : {
                          "show histogram" : self.af.show_bar_hist,
                          "contrast stretching" : self.af.stretch_hist,
                          "equalization" : self.af.equalization, 
                          "selective stretching" : self.af.create_selective_stretching_window,}, 
                  "calculate" : {
                          "moments" : self.af.create_moments_table,
                          "objects" : self.af.create_object_feature_vector_table,},
                  "watershed" : self.af.watershed,
                  "skeletonization" : self.af.skeletonization,
                  "morphological_operations" : self.af.create_morphological_operations_window,
                  "Hough" : self.af.detect_lines_hough},

        "Process":{
                  "median filter" : self.sp.create_median_filter_window, #TODO: bordery
                  "arithmetic operations" : {
                          "negation" : self.sp.negation, 
                          "posterize" : self.sp.posterize,
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
                          "blur" : self.sp.create_blur_window, #TODO: bordery
                          "laplacian" : self.sp.create_laplacian_window, #TODO: bordery
                          "canny" : self.sp.create_canny_window, #TODO: bordery
                          "sobel" : self.sp.create_sobel_window, #TODO: bordery
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
      mb = ttk.Menubutton(master = self.view, text = menu, bootstyle=(ttk.OUTLINE, ttk.SUCCESS))
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