from tkinter import *
import cv2 as cv 
import PIL
from numpy import *



class Image():
  def __init__(self, img = None, filepath = None):
    self.filepath = filepath
    if img is None:
      self.cv_img = self.read_image_in_format()
    else:
      self.cv_img = img
    self.format = self.set_format()
    self.tk_img = self.convert_to_tk_img()

  def read_image_in_format(self):
    if self.is_grey_scale():
      return cv.imread(self.filepath, cv.IMREAD_GRAYSCALE)
    else:
      return cv.imread(self.filepath)

  def is_grey_scale(self):
    img = cv.imread(self.filepath)
    w = img.shape[0] 
    h = img.shape[1]
    for i in range(w):
        for j in range(h):
            r, g, b = img[i,j]
            if r != g != b: 
                return False
    return True

  def convert_to_tk_img(self):
    if self.format == "RGB":
      blue, green, red = cv.split(self.cv_img)
      img = cv.merge((red, green, blue))
    else:
      img = self.cv_img
    cv_img = PIL.Image.fromarray(img)
    return PIL.ImageTk.PhotoImage(image=cv_img)
  
  def set_format(self):
    channels = len(self.cv_img.shape)
    if channels == 3:
      return "RGB"
    else:
      return "Gray" 