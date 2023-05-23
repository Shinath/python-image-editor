from view import *
from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk

class EditFunctions:
  def __init__(self, root):
    self.root = root
#TODO NIEDZIAŁA
  def convert_to_gray(self):
    active_window = self.root.active_window
    if active_window.image.format == "Gray":
      return
    rgb_img = active_window.image.cv_img
    gray_img = cv.cvtColor(rgb_img, cv.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(gray_img)
    pil_img = ImageTk.PhotoImage(pil_img)
    new_window = view.NewImageWindow(self.root, image = gray_img)
    new_window.title("Gray Conversion")
    new_window.show_image()