from tkinter import *
from view import *
import cv2 as cv
from tkinter import filedialog as fd
from image import Image
from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

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
    if filepath == '':
      return
    NewImageWindow(self.root, image_filepath = filepath).show_image()

  def info_window(self, event):
    NewWindow(self.root).show_info()

  def save(self):
    active_window = self.root.active_window
    filepath = active_window.image.filepath
    if filepath == None:
      self.save_as()
      return
    file = active_window.image.cv_img
    status = cv.imwrite(filepath, file)

    if not status:
      NewWindow(self.root, "Error").show_error("File has not been saved")
      
  def save_as(self):
    active_window = self.root.active_window
    files = [('All Files', '*.*')]
    filepath = fd.asksaveasfile(filetypes = files, defaultextension = files)
    file = active_window.image.cv_img
    status = cv.imwrite(filepath.name, file)

    if not status:
      NewWindow(self.root, "Error").show_error("File has not been saved")

    active_window.title(filepath.name)

  def convert_to_gray(self):
    active_window = self.root.active_window
    if active_window.image.format == "Gray":
      return
    rgb_img = active_window.image.cv_img
    gray_img = cv.cvtColor(rgb_img, cv.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(gray_img)
    pil_img = ImageTk.PhotoImage(pil_img)
    new_window = NewImageWindow(self.root, image = gray_img)
    new_window.title("Gray Convertion")
    new_window.show_image()

  def get_img_value_array(self):
    active_window = self.root.active_window
    if active_window.image.format == "RGB":
      new_window = NewWindow(self.root, title= "Error")
      new_window.show_error("Histograms are only for gray images")
      return False
    
    my_hist =np.zeros(256)
    img = active_window.image.cv_img
    for h in range(img.shape[0]):
      for w in range(img.shape[1]):
        current_pixel = img[h,w]
        my_hist[current_pixel] += 1
    return my_hist

  # show hist only for gray images
  def show_bar_hist(self):
    
    my_hist = self.get_img_value_array()
    if my_hist is False:
      return
    
    plt.bar([str(x) for x in range(256)], my_hist)
    plt.title("Histogram")
    plt.show()

  def split_channels(self):
    image = self.root.active_window.image
    if image.format != "RGB":
      new_window = NewWindow(self.root, title= "Error")
      new_window.show_error("This action is only for rgb images")
      return
    
    colors = cv.split(image.cv_img)
    titles = ["Blue", "Green", "Red"]
    i = 0
    for color in colors:
      nw = NewImageWindow(self.root, image= color)
      nw.title(titles[i])
      nw.show_image()
      i += 1

def generate_menubuttons(view):
    ff = FileFunctions(view)
    menu_dict = {
      "file" : { "load" : ff.load_image, "save" : ff.save, "save as..." : ff.save_as }, 
      "edit" : { "to gray" : ff.convert_to_gray },
      "show" : { "histogram" : ff.show_bar_hist },
      "process" : { "split channels" : ff.split_channels },
      "info" : ff.info_window,
      }
    for menu in menu_dict:
      if not isinstance(menu_dict[menu], dict):
        mb = Menubutton(master = view, text = menu, indicatoron=False, font=("Helvetica", 20))
        mb.bind("<Button-1>", menu_dict[menu])
      elif not menu_dict[menu]:
        mb = Menubutton(master = view, text = menu, indicatoron=False, font=("Helvetica", 20))
      else:
        mb = Menubutton(view, text=menu, indicatoron=False, font=("Helvetica", 20))
        mb.menu = Menu(mb)
        mb["menu"] = mb.menu
        for function_labels in menu_dict[menu]:
          mb.menu.add_command(label=function_labels, command = menu_dict[menu][function_labels], font=("Helvetica", 15))
      mb.pack(side = LEFT)