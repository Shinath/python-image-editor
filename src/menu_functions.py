from tkinter import *
from view import *
import cv2 as cv
from tkinter import filedialog as fd
from image import Image

class FileFunctions:
  def __init__(self, root):
    self.root = root

  def test_function(self):
    pass


  def load_image(self):
    filepath = fd.askopenfilename(
      filetypes=[("Image Files", ".bmp"),
                ("Image Files", ".jpg"),
                ("Image Files", ".tif"),
                ("Image Files", ".png"),
                ("All Files", "*.*")])
    #print(filepath)
    if filepath == None:
      #error handler TODO
      return
    else:
      NewImageWindow(self.root, image_filepath = filepath).show_image()

  def info_window(self, event):
    NewWindow(self.root).show_info()

  def save(self):
    active_window = self.root.active_window
    filepath = active_window.image.filepath
    if not filepath:
      #ERROr TODO there's nothing to save
      return
    file = active_window.image.cv_img
    status = cv.imwrite(filepath, file)

    if not status:
      pass #ERROR TODO file doesn't save
      
  def save_as(self):
    active_window = self.root.active_window
    files = [('All Files', '*.*')]
    filepath = fd.asksaveasfile(filetypes = files, defaultextension = files)
    file = active_window.image.cv_img
    status = cv.imwrite(filepath.name, file)

    if not status:
      pass #ERROR TODO file doesn't save

  def convert_to_shv(self):
    active_window = self.root.active_window
    active_window.image.cv_img
    hsv_img = cv.cvtColor(active_window.image.cv_img, cv.COLOR_RGB2HSV)
    new_window = NewImageWindow(self.root, image = hsv_img)
    new_window.title("HSC Convertion")
    new_window.show_image()
#zgrupuj 

def generate_menubuttons(view):
    ff = FileFunctions(view)
    menu_dict = {
      "file" : { "new" : ff.test_function, "load" : ff.load_image, "save" : ff.save, "save as..." : ff.save_as }, 
      "edit" : { "HSV" : ff.convert_to_shv },
      "show" : { "Histogram" : ff.test_function },
      "     " : None,
      "info" : ff.info_window,
      }
    for menu in menu_dict:
      if not isinstance(menu_dict[menu], dict):
        mb = Menubutton(master = view, text = menu, indicatoron=False)
        mb.bind("<Button-1>", menu_dict[menu])
      elif not menu_dict[menu]:
        mb = Menubutton(master = view, text = menu, indicatoron=False)
      else:
        mb = Menubutton(view, text=menu, indicatoron=False)
        mb.menu = Menu(mb)
        mb["menu"] = mb.menu
        for function_labels in menu_dict[menu]:
          mb.menu.add_command(label=function_labels, command = menu_dict[menu][function_labels])
      mb.pack(side = LEFT)