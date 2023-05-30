from tkinter import *
from tkinter import messagebox


class Validator:
  
  def validate_gray_image(window):
    if window.image.format == "RGB":
      messagebox.showerror("Wrong image format", "This function is only for gray images")
      return False
    return True

  def validate_rgb_image(window):
    if window.image.format == "Gray":
      messagebox.showerror("Wrong image format", "This functions is only for RGB images")