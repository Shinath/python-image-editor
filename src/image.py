from tkinter import *
import cv2 as cv 
import PIL
from numpy import *

class Image():
  def __init__(self, img, filepath):
    self.filepath = filepath
    self.cv_img = img
    self.format = self.set_format()
    self.tk_img = self.convert_to_tk_img()
    #print(self.format)

  def convert_to_tk_img(self):
    if self.format == "RGB":
      blue, green, red = cv.split(self.cv_img)
      img = cv.merge((red, green, blue))
      self.cv_img = PIL.Image.fromarray(img)
    return PIL.ImageTk.PhotoImage(image=self.cv_img)
  
  def set_format(self):
    channels = self.cv_img.shape[2]
    #print(channels)
    if channels == 3:
      return "RGB"
    else:
      return "grayscale" 