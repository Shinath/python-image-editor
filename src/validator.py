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
      messagebox.showerror("Wrong image format", "This function is only for RGB images")
      return False
    return True

  def validate_no_image(root):
    if len(root.winfo_children()) <= 5:
      messagebox.showerror("Image Not Selected", "Load images to proceed")
      return False
    return True

  def validate_not_the_same_window(window1, window2):
    if window1.get() == window2.get():
      messagebox.showerror("The same image", "Choose two different images to proceed")
      return False
    return True

  def validate_combobox(*args):
    for arg in args:
      if str(arg.get()) == '':
        messagebox.showerror("Empty combobox", "Choose options from all comboboxes")
        return True
    return False

  def validate_image_int_inputs(*args):
    try:
      for arg in args:
        number = int(arg.get())
        if number < 0:
          messagebox.showerror("Wrong input", "Values should be a positive number")
          return True
        if number > 255:
          messagebox.showerror("Wrong input", "Values should be a number smaller than 255")
    except:
      messagebox.showerror("Wrong input", "Values should be numbers")
      return True
    return False

  def validate_odd_number(number, label):
    if int(number.get()) % 2 == 0:
      messagebox.showerror("Wrong input", f"{label} must have an odd value")
      return True
    return False

  def validate_smaller_than_one_number(number, label):
    if int(number.get()) > 1:
      messagebox.showerror("Wrong input", f"{label} must have a value between 0 and 1")
      return True
    return False
