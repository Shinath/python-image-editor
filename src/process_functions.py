import cv2 as cv
import numpy as np
from tkinter import *
from view import *
import tkinter.ttk as ttk
import sys
from validator import *

np.set_printoptions(threshold=sys.maxsize)

class ProcessFunctions:

  def __init__(self, root) -> None:
    self.root = root
    self.border_dict = {'replicate' : cv.BORDER_REPLICATE,
                        'constant' : cv.BORDER_CONSTANT,
                        'reflect' : cv.BORDER_REFLECT}

  def create_blur_window(self):

    if not Validator.validate_no_image(self.root):
      return

    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    kernel_width = IntVar()
    kernel_hight = IntVar()
    ttk.Label(nw, text = "Kernel width: ").grid(row=0, column=0)
    ttk.Entry(nw, textvariable=kernel_width).grid(row=0, column=1)
    ttk.Label(nw, text= "Kernel hight: ").grid(row= 1, column=0)
    ttk.Entry(nw, textvariable=kernel_hight).grid(row=1, column=1)

    ttk.Label(nw, text= "Border type: ").grid(row= 2, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = list(self.border_dict.keys())
    combobox['state'] = 'readonly'
    combobox.grid(row=2, column=1)
    ttk.Button(nw, text= "Ok", command=lambda: self.blur(kernel_hight, kernel_width, combobox, img, nw)).grid(row=3, column=1, sticky= W)

  def blur(self, x, y, border_str ,img, nw):
    if Validator.validate_image_int_inputs(x, y):
      return

    if Validator.validate_combobox(border_str):
      return
    
    border_str = str(border_str.get())

    kernel_size = (int(x.get()),int(y.get()))
    border = self.border_dict[border_str]
    blured_img = cv.blur(img, kernel_size, borderType = border)
    NewImageWindow(self.root, blured_img).show_image()
    nw.destroy()

  def create_laplacian_window(self):

    if not Validator.validate_no_image(self.root):
      return

    if not Validator.validate_gray_image(self.root.active_window):
      return

    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    kernel_size = IntVar()
    ttk.Label(nw, text = "Kernel size: ").grid(row=0, column=0)
    ttk.Entry(nw, textvariable=kernel_size).grid(row=0, column=1)

    ttk.Label(nw, text= "Border type: ").grid(row= 1, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = list(self.border_dict.keys())
    combobox['state'] = 'readonly'
    combobox.grid(row=1, column=1)

    ttk.Button(nw, text= "Ok", command=lambda: self.laplacian(kernel_size, combobox, img, nw)).grid(row=2, column=1, sticky= W)

  def laplacian(self, ksize, border_str, img, nw):
    if Validator.validate_image_int_inputs(ksize):
      return 

    if Validator.validate_combobox(border_str):
      return
    
    border_str = str(border_str.get())
    ksize = int(ksize.get())
    ddepth = cv.CV_64F
    border = self.border_dict[border_str]
    img_laplacian = cv.Laplacian(img, ddepth, ksize, borderType = border)
    NewImageWindow(self.root, img_laplacian).show_image()
    nw.destroy()

  def create_sobel_window(self):

    if not Validator.validate_no_image(self.root):
      return

    if not Validator.validate_gray_image(self.root.active_window):
      return

    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    kernel_size = IntVar()
    ttk.Label(nw, text = "Kernel size: ").grid(row=0, column=0)
    ttk.Entry(nw, textvariable=kernel_size).grid(row=0, column=1)

    ttk.Button(nw, text= "Ok", command=lambda: self.sobel(kernel_size, img, nw)).grid(row=2, column=1, sticky= W)

  def sobel(self, ksize, img, nw):
    if Validator.validate_image_int_inputs(ksize) or Validator.validate_odd_number(ksize, "Kernel size"):
      return

    ksize = int(ksize.get())
    sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=ksize)
    sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=ksize)
    NewImageWindow(self.root, sobelx).show_image()
    NewImageWindow(self.root, sobely).show_image()
    nw.destroy()

  def create_canny_window(self):

    if not Validator.validate_no_image(self.root):
      return

    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    threshold1 = IntVar()
    threshold2 = IntVar()
    ttk.Label(nw, text = "threshold1: ").grid(row=0, column=0)
    ttk.Entry(nw, textvariable=threshold1).grid(row=0, column=1)
    ttk.Label(nw, text= "threshold2: ").grid(row= 1, column=0)
    ttk.Entry(nw, textvariable=threshold2).grid(row=1, column=1)
    ttk.Button(nw, text= "Ok", command=lambda: self.canny(threshold1, threshold2, img, nw)).grid(row=2, column=1, sticky= W)
  
  def canny(self, t1, t2, img, nw):
    if Validator.validate_image_int_inputs(t1, t2):
      return

    t1 = int(t1.get())
    t2 = int(t2.get())
    img_canny = cv.Canny(img, t1, t2)
    NewImageWindow(self.root, img_canny).show_image()
    nw.destroy()

  def create_linear_sharpening_window(self):

    if not Validator.validate_no_image(self.root):
      return

    if not Validator.validate_gray_image(self.root.active_window):
      return

    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)

    ttk.Label(nw, text= "mask: ").grid(row=0, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = ('mask1', 'mask2', 'mask3')
    combobox['state'] = 'readonly'
    combobox.grid(row=0, column=1)

    ttk.Label(nw, text= "Border type: ").grid(row= 1, column=0)
    current_var2 = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=current_var2)
    combobox2['values'] = list(self.border_dict.keys())
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)
    ttk.Button(nw, text= "Ok", command=lambda: self.linear_sharpening(combobox, combobox2, img, nw)).grid(row=2, column=1, sticky= W)

  def linear_sharpening(self, mask_label, border_str, img, nw):

    if Validator.validate_combobox(mask_label, border_str):
      return

    mask_label = str(mask_label.get())
    border_str = str(border_str.get())

    mask_dict = { 'mask1' : np.array([[ 0,-1, 0],[-1, 5,-1],[ 0,-1, 0]]),
                  'mask2' : np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]]),
                  'mask3' : np.array([[ 1,-2, 1],[-2, 5,-2],[ 1,-2, 1]])}
    border = self.border_dict[border_str]
    mask_sharp = mask_dict[mask_label]
    img_sharp = cv.filter2D(img,cv.CV_64F, mask_sharp, borderType = border)
    NewImageWindow(self.root, img_sharp).show_image()
    nw.destroy()
    
  def create_edge_detection_window(self):

    if not Validator.validate_no_image(self.root):
          return
    if not Validator.validate_gray_image(self.root.active_window):
      return

    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)

    ttk.Label(nw, text= "direction: ").grid(row=0, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')
    combobox['state'] = 'readonly'
    combobox.grid(row=0, column=1)

    ttk.Label(nw, text= "Border type: ").grid(row= 1, column=0)
    current_var2 = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=current_var2)
    combobox2['values'] = list(self.border_dict.keys())
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    ttk.Button(nw, text= "Ok", command=lambda: self.edge_detection(combobox, combobox2, img, nw)).grid(row=2, column=1, sticky= W)
  
  def edge_detection(self, direction_string, border_str, img, nw):

    if Validator.validate_combobox(direction_string, border_str):
      return

    direction_string = str(direction_string.get())
    border_str = str(border_str.get())

    direction_dict = {'N' : np.array([[1,1,1],[1,-2,+1],[-1,-1,-1]]),
                      'NE' : np.array([[0,+1,+1],[-1,0,+1],[-1,-1,0]]),
                      'E' : np.array([[-1,+1,+1],[-1,-2,+1],[-1,1,1]]),
                      'SE' : np.array([[-1,-1,0],[-1,0,+1],[0,1,1]]),
                      'S' : np.array([[-1,-1,-1],[1,-2,+1],[1,1,1]]),
                      'SW' : np.array([[0,-1,-1],[1,0,-1],[1,1,0]]),
                      'W' : np.array([[1,+1,-1],[1,-2,-1],[1,1,-1]]),
                      'NW' : np.array([[1,+1,0],[1,0,+1],[0,-1,-1]])}

    direction = direction_dict[direction_string]
    border = self.border_dict[border_str]
    img_prewitt = cv.filter2D(img, cv.CV_64F, direction, borderType = border)
    NewImageWindow(self.root, img_prewitt).show_image()
    nw.destroy()

  def create_median_filter_window(self):

    if not Validator.validate_no_image(self.root):
      return

    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    ttk.Label(nw, text= "window size: ").grid(row=0, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = ('3x3', '5x5', '7x7')
    combobox['state'] = 'readonly'
    combobox.grid(row=0, column=1)
    ttk.Button(nw, text= "Ok", command=lambda: self.median_filter(combobox, img, nw)).grid(row=1, column=1, sticky= W)
  
  def median_filter(self, size_string, img, nw):

    if Validator.validate_combobox(size_string):
      return

    size_string = str(size_string.get())
    print(size_string)
    size_dict = {'3x3' : 3, '5x5' : 5, '7x7' : 7}
    size = size_dict[size_string]
    median_img = cv.medianBlur(img, size)
    NewImageWindow(self.root, median_img).show_image()
    nw.destroy()
  
  def create_logic_operation_window(self, func):

    if not Validator.validate_no_image(self.root):
      return

    nw = NewWindow(self.root)
    ttk.Label(nw, text= "First image: ").grid(row=0, column=0)
    windows = [window for window in self.root.winfo_children() if isinstance(window, NewImageWindow)]

    current_var1 = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=current_var1)
    combobox1['values'] = windows
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    ttk.Label(nw, text= "Second image: ").grid(row=1, column=0)
    
    current_var2 = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=current_var2)
    combobox2['values'] = windows
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    ttk.Button(nw, text= "Ok", command=lambda: func(combobox1, combobox2, nw)).grid(row=2, column=1, rowspan=2, columnspan=3, sticky= W)

  def addition(self, window1, window2, nw): 

    if Validator.validate_combobox(window1, window2):
      return

    if not Validator.validate_not_the_same_window(window1, window2):
      return

    window1 = str(window1.get())
    window2 = str(window2.get())

    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]

    if not Validator.validate_gray_image(window1[0]):
      return

    if not Validator.validate_gray_image(window2[0]):
      return
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.add(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()

  def subtraction(self, window1, window2, nw):
    if Validator.validate_combobox(window1, window2):
      return

    if not  Validator.validate_not_the_same_window(window1, window2):
      return

    window1 = str(window1.get())
    window2 = str(window2.get())
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    if not Validator.validate_gray_image(window1[0]):
      return

    if not Validator.validate_gray_image(window2[0]):
      return
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.subtract(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()

  def bitwise_and(self, window1, window2, nw):
    if Validator.validate_combobox(window1, window2):
      return

    if not  Validator.validate_not_the_same_window(window1, window2):
      return

    window1 = str(window1.get())
    window2 = str(window2.get())

    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    if not Validator.validate_gray_image(window1[0]):
      return

    if not Validator.validate_gray_image(window2[0]):
      return
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.bitwise_and(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()
  
  def bitwise_or(self, window1, window2, nw):
    if Validator.validate_combobox(window1, window2):
      return

    if not  Validator.validate_not_the_same_window(window1, window2):
      return

    window1 = str(window1.get())
    window2 = str(window2.get())
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    if not Validator.validate_gray_image(window1[0]):
      return

    if not Validator.validate_gray_image(window2[0]):
      return
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.bitwise_or(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()
  
  def bitwise_xor(self, window1, window2, nw):
    if Validator.validate_combobox(window1, window2):
      return

    if not Validator.validate_not_the_same_window(window1, window2):
      return

    window1 = str(window1.get())
    window2 = str(window2.get())
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    if not Validator.validate_gray_image(window1[0]):
      return

    if not Validator.validate_gray_image(window2[0]):
      return
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.bitwise_xor(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()
  
  def creating_blending_window(self):

    if not Validator.validate_no_image(self.root):
      return
    nw = NewWindow(self.root)
    ttk.Label(nw, text= "First image: ").grid(row=0, column=0)
    windows = [window for window in self.root.winfo_children() if isinstance(window, NewImageWindow)]

    current_var1 = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=current_var1)
    combobox1['values'] = windows
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    ttk.Label(nw, text= "Second image: ").grid(row=1, column=0)
    
    current_var2 = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=current_var2)
    combobox2['values'] = windows
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    alpha = IntVar()
    beta = IntVar()
    gamma = IntVar()

    ttk.Label(nw, text= "alpha: ").grid(row=2, column=0)
    ttk.Entry(nw, textvariable=alpha).grid(row=2, column=1)
    ttk.Label(nw, text= "beta: ").grid(row=3, column=0)
    ttk.Entry(nw, textvariable=beta).grid(row=3, column=1)
    ttk.Label(nw, text= "gamma: ").grid(row=4, column=0)
    ttk.Entry(nw, textvariable=gamma).grid(row=4, column=1)

    ttk.Button(nw, text= "Ok", command=lambda: 
      self.blending(combobox1, combobox2, alpha,
      beta, gamma, nw)).grid(row=5, column=1, sticky= W)


  def blending(self, window1, window2, alpha, beta, gamma, nw):

    if Validator.validate_image_int_inputs(alpha, beta, gamma):
      return 

    if Validator.validate_combobox(window1, window2):
      return

    if not Validator.validate_not_the_same_window(window1, window2):
      return

    if Validator.validate_smaller_than_one_number(alpha, "alpha"):
      return

    if Validator.validate_smaller_than_one_number(beta, "beta"):
      return

    window1 = str(window1.get())
    window2 = str(window2.get())

    alpha= int(alpha.get())
    beta= int(beta.get())
    gamma= int(gamma.get())
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    if not Validator.validate_gray_image(window1[0]):
      return

    if not Validator.validate_gray_image(window2[0]):
      return
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)
    img_blend = cv.addWeighted(img1, alpha, img2, beta, gamma)
    NewImageWindow(self.root, img_blend).show_image()
    nw.destroy()

  def create_thresholding_window(self):

    if not Validator.validate_no_image(self.root):
      return
    window = self.root.active_window

    nw = NewWindow(self.root)
    ttk.Label(nw, text='thresholding level: ').grid(row=0, column=0)
    scale = Scale(nw, from_=0, to=255, orient=HORIZONTAL)
    scale.grid(row=0, column=1)
    button = ttk.Button(nw, text="Ok")
    button.grid(row=1, column=0)
    scale.config(command= lambda value: self.thresholding(window, button, nw, int(value)))

  def thresholding(self, window, button, nw, thresh = 0): 
    def on_closing(nw):
      window.refresh_image(window.image.cv_img)
      nw.destroy()
    nw.protocol("WM_DELETE_WINDOW",lambda: on_closing(nw))
    _,img_th_binary = cv.threshold(window.image.cv_img, thresh, 255, cv.THRESH_BINARY)
    window.refresh_image(img_th_binary)
    button.config(command= lambda: window.save_new_image(img_th_binary, nw))


  def create_adaptive_thresholging_window(self):
    if not Validator.validate_no_image(self.root):
      return

    if not Validator.validate_gray_image(self.root.active_window):
      return
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    
    ttk.Label(nw, text= "adaptive method: ").grid(row=0, column=0)
    methods = ['mean c', 'gaussian']

    method = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=method)
    combobox1['values'] = methods
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    ttk.Label(nw, text= "threshold type: ").grid(row=1, column=0)
    types = ['binary', 'binary inversion']

    type = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=type)
    combobox2['values'] = types
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    ttk.Label(nw, text='block size: ').grid(row=2, column=0)
    block = IntVar()
    ttk.Entry(nw, textvariable=block).grid(row=2, column=1)

    ttk.Button(nw, text='Ok', command=lambda: self.adaptive_thresholding(method, type, block, img, nw)).grid(row=3, column=0)

  def adaptive_thresholding(self, method, type, block, img, nw):

    if Validator.validate_combobox(method, type):
      return

    if  Validator.validate_image_int_inputs(block) or Validator.validate_odd_number(block, "block size"):
      return 

    method = str(method.get())
    type = str(type.get())

    block = int(block.get())
    methods = {'mean c' : cv.ADAPTIVE_THRESH_MEAN_C, 'gaussian' : cv.ADAPTIVE_THRESH_GAUSSIAN_C }
    method = methods[method]

    types = {'binary' : cv.THRESH_BINARY, 'binary inversion' : cv.THRESH_BINARY_INV}
    type = types[type]
    
    img_th_adapt = cv.adaptiveThreshold(img, 255, method, type, block, 5)
    NewImageWindow(self.root, img_th_adapt).show_image()
    nw.destroy()

  def otsus_thresholding(self):
    if not Validator.validate_no_image(self.root):
      return

    if not Validator.validate_gray_image(self.root.active_window):
      return
    img = self.root.active_window.image.cv_img
    blur = cv.GaussianBlur(img,(5,5),0)
    _,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    NewImageWindow(self.root, th3).show_image()


  def negation(self):
    if not Validator.validate_no_image(self.root):
      return
    if not Validator.validate_gray_image(self.root.active_window):
      return

    img = self.root.active_window.image.cv_img
    img_inv = (255 - img)
    NewImageWindow(self.root, img_inv).show_image()

  def posterize(self):
    if not Validator.validate_no_image(self.root):
      return
    if not Validator.validate_gray_image(self.root.active_window):
      return

    img = self.root.active_window.image.cv_img

    nw = NewWindow(self.root)
    bins_length = IntVar()
    bins_number = IntVar()
    ttk.Label(nw, text = "Numbers of Bins: ").grid(row=0, column=0)
    ttk.Entry(nw, textvariable=bins_number).grid(row=0, column=1)
    ttk.Label(nw, text= "Bin length: ").grid(row= 1, column=0)
    ttk.Entry(nw, textvariable=bins_length).grid(row=1, column=1)
    ttk.Button(nw, text= "Ok", command=lambda: self.posterize_on_button_click(bins_number, bins_length, img, nw)).grid(row=2, column=1, sticky= W)
  
  
  def posterize_on_button_click(self, bins_number, bins_length, img, nw):
  
    if Validator.validate_image_int_inputs(bins_length, bins_number):
      return

    bins_length = int(bins_length.get())
    bins_number = int(bins_number.get())

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
    