from view import NewImageWindow
from tkinter import *
import cv2 as cv
import PIL as pl
from validator import *

class EditFunctions:
  def __init__(self, root):
    self.root = root


  def convert_to_gray(self):
    if not Validator.validate_no_image(self.root):
      return 1
    active_window = self.root.active_window
    if active_window.image.format == "Gray":
      return 1
    rgb_img = active_window.image.cv_img
    gray_img = cv.cvtColor(rgb_img, cv.COLOR_BGR2GRAY)
    pil_img = pl.Image.fromarray(gray_img)
    pil_img = pl.ImageTk.PhotoImage(pil_img)
    new_window = NewImageWindow(self.root, image = gray_img)
    new_window.title("Gray Conversion")
    new_window.show_image()

  def split_channels(self):
    if not Validator.validate_no_image(self.root):
      return 1
    image = self.root.active_window.image
    
    if not Validator.validate_rgb_image(self.root.active_window):
      return 1
    
    colors = cv.split(image.cv_img)
    titles = ["Blue", "Green", "Red"]
    i = 0
    for color in colors:
      nw = NewImageWindow(self.root, image= color)
      nw.title(titles[i])
      nw.show_image()
      i += 1