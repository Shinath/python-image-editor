from show_functions import *
import numpy as np
import matplotlib.pyplot as plt

class ProcessFunctions:
  def __init__(self, root):
    self.root = root

  def stretch_hist(self):

    if self.root.active_window.image.format == "RGB":
      messagebox.showerror("Error", "Histograms are only for gray images")
      return 

    img = self.root.active_window.image.cv_img
    img_min = np.min(img)
    img_max = np.max(img)
    new_max = 255
    img_stretch =np.zeros_like(img)
    for h in range(img.shape[0]):
      for w in range(img.shape[1]):
        current_pixel = img[h,w]
        img_stretch[h,w] = ((current_pixel-img_min)*new_max)/(img_max-img_min)
    NewImageWindow(self.root, image=img_stretch).show_image()

  def equalization(self):

    if self.root.active_window.image.format == "RGB":
      messagebox.showerror("Error", "Histograms are only for gray images")
      return 

    img = self.root.active_window.image.cv_img
    sf = ShowFunctions(self.root)
    cs = cumsum(sf.get_img_value_array())
    cs_min = cs.min()
    cs_max = cs.max()
    cs = ((cs - cs_min) * 255 )/ (cs_max - cs_min)
    img_eq = cs[img]
    NewImageWindow(self.root, img_eq).show_image()

  def negation(self):
    if self.root.active_window.image.format == "RGB":
      messagebox.showerror("Error", "Histograms are only for gray images")
      return 

    img = self.root.active_window.image.cv_img
    img_inv = (255 - img)
    NewImageWindow(self.root, img_inv).show_image()

  # TODO
  def on_scale_change (self, value, active_window):

      value = int(value)
      if active_window.image.format == "RGB":
            messagebox.showerror("Error", "Histograms are only for gray images")
            return 

      img = active_window.image.cv_img
      img_th = np.zeros_like(img)

      for h in range(img.shape[0]):
        for w in range(img.shape[1]):
          current_pixel = img[h,w]
          if (current_pixel>127): img_th[h,w]=255
      
      active_window.image.cv_img = img_th
      active_window.image.convert_to_tk_img()
      active_window.refresh_image()
      #NewImageWindow(self.root, img_th).show_image()

  #TODO
  def thresholding(self):
    nw = NewWindow(self.root)
    nw.geometry("300x300")
    scale = Scale(nw, from_=0, to=255, orient=HORIZONTAL, resolution=5)
    scale.config(command=lambda value: self.on_scale_change(value, self.root.active_window))
    scale.pack()


  def posterize(self):
    if self.root.active_window.image.format == "RGB":
      messagebox.showerror("Error", "Histograms are only for gray images")
      return 

    img = self.root.active_window.image.cv_img

    nw = NewWindow(self.root)
    bins_length = IntVar()
    bins_number = IntVar()
    Label(nw, text = "Numbers of Bins: ").grid(row=0, column=0)
    Entry(nw, textvariable=bins_number).grid(row=0, column=1)
    Label(nw, text= "Bin length: ").grid(row= 1, column=0)
    Entry(nw, textvariable=bins_length).grid(row=1, column=1)
    Button(nw, text= "Ok", command=lambda: self.posterize_on_button_click(bins_number, bins_length, img, nw)).grid(row=2, column=1, sticky= W)
    
  def posterize_on_button_click(self, bins_number, bins_length, img, nw):
    
    try: 
      bins_length = int(bins_length.get())
      bins_number = int(bins_number.get())

      if bins_length > 255 or bins_length < 0:
        raise
      if bins_number > 255 or bins_number < 0:
        raise

    except:
      messagebox.showerror("Error", "Wrong, try again!")
      return

    bins = np.arange(0,255,np.round(255/bins_number))
    img_pstrz = np.zeros_like(img)
    for h in range(img.shape[0]):
      for w in range(img.shape[1]):
        current_pixel = img[h,w]
    
        for bin in range(bins_number):
          if (current_pixel>bins[bin]): img_pstrz[h,w]=bins[bin]

        if (current_pixel>bins[-1]): img_pstrz[h,w]=255

    NewImageWindow(self.root, img_pstrz).show_image()
    nw.destroy()
      

# -------------------------------------

def cumsum(a):
  a = iter(a)
  b = [next(a)]
  for i in a:
      b.append(b[-1] + i)
  return np.array(b)