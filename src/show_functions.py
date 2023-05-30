from tkinter import *
from tkinter import messagebox
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from view import *
from validator import *

class ShowFunctions:
  def __init__(self, root):
    self.root = root

  # show hist only for gray images
  def show_bar_hist(self):
    
    my_hist = self.get_img_value_array()
    if my_hist is False:
      return
    
    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    plot.bar([str(x) for x in range(256)], my_hist)
    nw = NewWindow(self.root)
    canvas = FigureCanvasTkAgg(figure, master = nw)
    canvas.draw()
    canvas.get_tk_widget().pack()

  def split_channels(self):
    image = self.root.active_window.image
    if image.format != "RGB":
      messagebox.showerror("Error", "This action is only for rgb images", icon='error')
      return
    
    colors = cv.split(image.cv_img)
    titles = ["Blue", "Green", "Red"]
    i = 0
    for color in colors:
      nw = NewImageWindow(self.root, image= color)
      nw.title(titles[i])
      nw.show_image()
      i += 1

def get_img_value_array(window):
  
  if not Validator.validate_gray_image(window):
    return False
  
  my_hist= np.zeros(256)
  img= window.image.cv_img
  for h in range(img.shape[0]):
    for w in range(img.shape[1]):
      current_pixel= img[h,w]
      my_hist[int(current_pixel)] += 1
  return my_hist