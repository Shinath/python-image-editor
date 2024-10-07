from tkinter import *
from tkinter import messagebox
from view import *
from tkinter import filedialog as fd

class FileFunctions:
  def __init__(self, root):
    self.root = root


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
    messagebox.showinfo("Info", "Autor: Wiktoria Kalata\n Prowadzący: mgr. inz. Roszkowiak Łukasz")

  def save(self):
    active_window = self.root.active_window
    filepath = active_window.image.filepath
    if filepath == None:
      self.save_as()
      return
    file = active_window.image.cv_img
    status = cv.imwrite(filepath, file)

    if not status:
      messagebox.showerror("Error", "File has not been saved")
  
  def save_as(self):
    active_window = self.root.active_window
    files = [('All Files', '*.*')]
    filepath = fd.asksaveasfile(filetypes = files, defaultextension = files)
    file = active_window.image.cv_img
    status = cv.imwrite(filepath.name, file)

    if not status:
      messagebox.showerror("Error", "File has not been saved")
      return
    active_window.title(filepath.name)