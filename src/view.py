from tkinter import *
import cv2 as cv 
import image as img
import ttkbootstrap as ttk
import PIL


class View(Tk):
  def __init__(self) -> None:
    super().__init__()
    self.resizable(False, False)
    self.active_window = None
    self.title("APO")


  def change_active_window(self, event):
    active_windows = event.widget
    for window in [x for x in self.winfo_children() if isinstance(x, NewImageWindow)]:
      if active_windows == window:
        self.active_window = window

class NewWindow(Toplevel):
  def __init__(self, master, title = "", *args, **kwargs):
    super().__init__(master, *args, **kwargs)
    self.title(title)
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)
    self.resizable(False, False)
    

class NewImageWindow(NewWindow):
  def __init__(self, master, image = None, image_filepath = None, *args, **kwargs):
    super().__init__(master, image_filepath, *args, **kwargs)
    self.bind("<FocusIn>", master.change_active_window)
    self.image = img.Image(image, image_filepath)

  def show_image(self):
    label = Label(self, image=self.image.tk_img)
    label.grid(row=0, column=0, sticky=N+S+E+W)
  
  def refresh_image(self, image):
    label = self.winfo_children()[0]
    cv_img = img.Image.convert_to_tk_img(image, 'Grey')
    label.configure(image = cv_img)
    label.image = cv_img

  def save_new_image(self, image, nw):
    self.image = img.Image(image)
    nw.destroy()
