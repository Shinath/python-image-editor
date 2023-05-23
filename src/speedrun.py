import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from show_functions import *
import tkinter.ttk as ttk

class Speedrun:

  def __init__(self, root) -> None:
    self.root = root

  def create_blur_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    kernel_width = IntVar()
    kernel_hight = IntVar()
    Label(nw, text = "Kernel width: ").grid(row=0, column=0)
    Entry(nw, textvariable=kernel_width).grid(row=0, column=1)
    Label(nw, text= "Kernel hight: ").grid(row= 1, column=0)
    Entry(nw, textvariable=kernel_hight).grid(row=1, column=1)
    Button(nw, text= "Ok", command=lambda: self.blur(kernel_hight, kernel_width, img, nw)).grid(row=2, column=1, sticky= W)

  def blur(self, x, y, img, nw):
    kernel_size = (int(x.get()),int(y.get()))
    blured_img = cv.blur(img, kernel_size, borderType = cv.BORDER_REPLICATE)
    NewImageWindow(self.root, blured_img).show_image()
    nw.destroy()

  def create_laplacian_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    kernel_size = IntVar()
    Label(nw, text = "Kernel size: ").grid(row=0, column=0)
    Entry(nw, textvariable=kernel_size).grid(row=0, column=1)
    Button(nw, text= "Ok", command=lambda: self.laplacian(int(kernel_size.get()), img, nw)).grid(row=2, column=1, sticky= W)

  def laplacian(self, ksize, img, nw):
    ddepth = cv.CV_64F
    img_laplacian = cv.Laplacian(img, ddepth, ksize, borderType = cv.BORDER_REPLICATE)
    NewImageWindow(self.root, img_laplacian).show_image()
    nw.destroy()

  def create_sobel_window(self, func):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    kernel_size = IntVar()
    Label(nw, text = "Kernel size: ").grid(row=0, column=0)
    Entry(nw, textvariable=kernel_size).grid(row=0, column=1)
    Button(nw, text= "Ok", command=lambda: self.sobel(int(kernel_size.get()), img, nw)).grid(row=2, column=1, sticky= W)

  def sobel(self, ksize, img, nw):
    sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=ksize)
    sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=ksize)
    frame_sobel = cv2.hconcat((sobelx, sobely))
    NewImageWindow(self.root, frame_sobel).show_image()
    nw.destroy()

  def create_canny_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    threshold1 = IntVar()
    threshold2 = IntVar()
    Label(nw, text = "threshold1: ").grid(row=0, column=0)
    Entry(nw, textvariable=threshold1).grid(row=0, column=1)
    Label(nw, text= "threshold2: ").grid(row= 1, column=0)
    Entry(nw, textvariable=threshold2).grid(row=1, column=1)
    Button(nw, text= "Ok", command=lambda: self.canny(int(threshold1.get()), int(threshold2.get()), img, nw)).grid(row=2, column=1, sticky= W)
  
  def canny(self, t1, t2, img, nw):
    img_canny = cv.Canny(img, t1, t2)
    NewImageWindow(self.root, img_canny).show_image()
    nw.destroy()

  def create_linear_sharpening_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)

    Label(nw, text= "mask: ").grid(row=0, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = ('mask1', 'mask2', 'mask3')
    combobox['state'] = 'readonly'
    combobox.grid(row=0, column=1)
    Button(nw, text= "Ok", command=lambda: self.linear_sharpening(str(combobox.get()), img, nw)).grid(row=2, column=1, sticky= W)

  def linear_sharpening(self, mask_label, img, nw):
      mask_dict = { 'mask1' : np.array([[ 0,-1, 0],[-1, 5,-1],[ 0,-1, 0]]),
                    'mask2' : np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]]),
                    'mask3' : np.array([[ 1,-2, 1],[-2, 5,-2],[ 1,-2, 1]])}  
      mask_sharp = mask_dict[mask_label]
      img_sharp = cv.filter2D(img,cv.CV_64F, mask_sharp, borderType = cv.BORDER_REPLICATE)
      NewImageWindow(self.root, img_sharp).show_image()
      nw.destroy()
    
  def create_edge_detection_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)

    Label(nw, text= "direction: ").grid(row=0, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')
    combobox['state'] = 'readonly'
    combobox.grid(row=0, column=1)
    Button(nw, text= "Ok", command=lambda: self.edge_detection(str(combobox.get()), img, nw)).grid(row=2, column=1, sticky= W)
  
  def edge_detection(self, direction_string, img, nw):
    direction_dict = {'N' : np.array([[1,1,1],[1,-2,+1],[-1,-1,-1]]),
                      'NE' : np.array([[0,+1,+1],[-1,0,+1],[-1,-1,0]]),
                      'E' : np.array([[-1,+1,+1],[-1,-2,+1],[-1,1,1]]),
                      'SE' : np.array([[-1,-1,0],[-1,0,+1],[0,1,1]]),
                      'S' : np.array([[-1,-1,-1],[1,-2,+1],[1,1,1]]),
                      'SW' : np.array([[0,-1,-1],[1,0,-1],[1,1,0]]),
                      'W' : np.array([[1,+1,-1],[1,-2,-1],[1,1,-1]]),
                      'NW' : np.array([[1,+1,0],[1,0,+1],[0,-1,-1]])}

    direction = direction_dict[direction_string]
    img_prewitt = cv.filter2D(img, cv.CV_64F, direction, borderType = cv.BORDER_REPLICATE)
    NewImageWindow(self.root, img_prewitt).show_image()
    nw.destroy()

  def create_median_filter_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    Label(nw, text= "window size: ").grid(row=0, column=0)
    current_var = StringVar()
    combobox = ttk.Combobox(nw, textvariable=current_var)
    combobox['values'] = ('3x3', '5x5', '7x7')
    combobox['state'] = 'readonly'
    combobox.grid(row=0, column=1)
    Button(nw, text= "Ok", command=lambda: self.linear_sharpening(str(combobox.get()), img, nw)).grid(row=2, column=1, sticky= W)
  
  def median_filter(self, size_string, img, nw):
    size_dict = {'3x3' : 3, '5x5' : 5, '7x7' : 7}
    size = size_dict[size_string]
    median_img = cv.medianBlur(img, size)
    NewImageWindow(self.root, median_img).show_image()
    nw.destroy()
  
  def create_logic_operation_window(self, func):
    nw = NewWindow(self.root)
    Label(nw, text= "First image: ").grid(row=0, column=0)
    windows = [window for window in self.root.winfo_children() if isinstance(window, NewImageWindow)]

    current_var1 = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=current_var1)
    combobox1['values'] = windows
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    Label(nw, text= "Second image: ").grid(row=1, column=0)
    
    current_var2 = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=current_var2)
    combobox2['values'] = windows
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    Button(nw, text= "Ok", command=lambda: func(combobox1.get(), combobox2.get(), nw)).grid(row=2, column=1, sticky= W)

  def addition(self, window1, window2, nw):
    #TODO walidacja obrazów czy oba są szaroodcieniowe
    
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.add(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()

  def subtraction(self, window1, window2, nw):
    #TODO walidacja obrazów czy oba są szaroodcieniowe
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.subtract(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()

  def bitwise_and(self, window1, window2, nw):
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.bitwise_and(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()
  
  def bitwise_or(self, window1, window2, nw):
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.bitwise_or(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()
  
  def bitwise_xor(self, window1, window2, nw):
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)

    img = cv.bitwise_xor(img1, img2)
    NewImageWindow(self.root, img).show_image()
    nw.destroy()
  
  def creating_blending_window(self):
    #TODO walidacja obrazów czy oba są szaroodcieniowe, walidacja inputów

    nw = NewWindow(self.root)
    Label(nw, text= "First image: ").grid(row=0, column=0)
    windows = [window for window in self.root.winfo_children() if isinstance(window, NewImageWindow)]

    current_var1 = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=current_var1)
    combobox1['values'] = windows
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    Label(nw, text= "Second image: ").grid(row=1, column=0)
    
    current_var2 = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=current_var2)
    combobox2['values'] = windows
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    alpha = IntVar()
    beta = IntVar()
    gamma = IntVar()

    Label(nw, text= "alpha: ").grid(row=2, column=0)
    Entry(nw, textvariable=alpha).grid(row=2, column=1)
    Label(nw, text= "beta: ").grid(row=3, column=0)
    Entry(nw, textvariable=alpha).grid(row=3, column=1)
    Label(nw, text= "gamma: ").grid(row=4, column=0)
    Entry(nw, textvariable=alpha).grid(row=4, column=1)

    Button(nw, text= "Ok", command=lambda: 
      self.blending(str(combobox1.get()), str(combobox2.get()), int(alpha.get()),
      int(beta.get()), int(gamma.get()), nw)).grid(row=5, column=1, sticky= W)


  def blending(self, window1, window2, alpha, beta, gamma, nw):
    #TODO walidacja
    window1 = [x for x in self.root.winfo_children() if window1 == str(x)]
    window2 = [x for x in self.root.winfo_children() if window2 == str(x)]
    img1 = window1[0].image.cv_img
    img2 = cv.resize(window2[0].image.cv_img, img1.shape)
    img_blend = cv.addWeighted(img1, alpha, img2, beta, gamma)
    NewImageWindow(self.root, img_blend).show_image()
    nw.destroy()