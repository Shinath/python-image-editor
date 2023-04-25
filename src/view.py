from tkinter import *
import cv2 as cv 
import image as img
from PIL import Image, ImageTk

class View(Tk):
  def __init__(self) -> None:
    super().__init__()
    self.resizable(False, False)
    self.active_window = None


  def change_active_window(self, event):
    active_windows = event.widget
    for window in self.winfo_children():
      if active_windows == window:
        self.active_window = window


class NewWindow(Toplevel):
  def __init__(self, master, title = "", *args, **kwargs):
    super().__init__(master, *args, **kwargs)
    self.title(title)
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)

  def show_info(self):
    self.geometry('300x300')
    Label(self, text= "Autor: Wiktoria Kalata").pack()

  def show_error(self, text):
    Label(self, text= text, font = ("Helvetica", 15)).pack(padx=10, pady=10, anchor=CENTER)
    self.grab_set()



class NewImageWindow(NewWindow):
  def __init__(self, master, image = None, image_filepath = None, *args, **kwargs):
    super().__init__(master, image_filepath, *args, **kwargs)
    self.bind("<FocusIn>", master.change_active_window)
    self.title(image_filepath)
    self.image = img.Image(image, image_filepath)

  def show_image(self):
    label = Label(self, image=self.image.tk_img)
    label.grid(row=0, column=0, sticky=N+S+E+W)
    
