import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from show_functions import *
import tkinter.ttk as ttk
import random
import sys

np.set_printoptions(threshold=sys.maxsize)

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

  def create_sobel_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    kernel_size = IntVar()
    Label(nw, text = "Kernel size: ").grid(row=0, column=0)
    Entry(nw, textvariable=kernel_size).grid(row=0, column=1)
    Button(nw, text= "Ok", command=lambda: self.sobel(int(kernel_size.get()), img, nw)).grid(row=2, column=1, sticky= W)

  def sobel(self, ksize, img, nw):
    sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=ksize)
    sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=ksize)
    frame_sobel = cv.hconcat((sobelx, sobely))
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
    Entry(nw, textvariable=beta).grid(row=3, column=1)
    Label(nw, text= "gamma: ").grid(row=4, column=0)
    Entry(nw, textvariable=gamma).grid(row=4, column=1)

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


  # ------ lab 4 -------

  def create_morphological_operations_window(self):
    img = self.root.active_window.image.cv_img

    nw = NewWindow(self.root)

    Label(nw, text= "Operation: ").grid(row=0, column=0)

    operation = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=operation)
    combobox1['values'] = ['erode', 'dilate', 'open', 'close']
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    Label(nw, text= "Shape: ").grid(row=1, column=0)

    shape = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=shape)
    combobox2['values'] = ['square', 'diamond']
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    Label(nw, text= "Size: ").grid(row=3, column=0)

    size = IntVar()
    Entry(nw, textvariable=size).grid(row=3, column=1)

    Label(nw, text= "Border: ").grid(row=4, column=0)

    border_type = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=border_type)
    combobox2['values'] = ['replicate', 'constant', 'reflect']
    combobox2['state'] = 'readonly'
    combobox2.grid(row=4, column=1)

    Button(nw, text= "Ok", command=lambda: 
      self.morphological_operations(str(operation.get()), str(shape.get()), int(size.get()),
      str(border_type.get()), img, nw)).grid(row=5, column=1, sticky= W)

  def morphological_operations(self, operation_str, shape_str, size, border_str, img, nw):

    operation_dict = {'erode' : cv.MORPH_ERODE, 'dilate' : cv.MORPH_DILATE,
                      'open' : cv.MORPH_OPEN, 'close' : cv.MORPH_CLOSE}
    operation = operation_dict[operation_str]

    shape_dict = {'square' : cv.getStructuringElement(cv.MORPH_RECT, (size, size)),
                  'diamond' : diamond(size)}
    shape = shape_dict[shape_str] #TODO

    border_dict = {'replicate' : cv.BORDER_REPLICATE,
                  'constant' : cv.BORDER_CONSTANT,
                  'reflect' : cv.BORDER_REFLECT}
    border = border_dict[border_str]

    img_morph = cv.morphologyEx(img, operation, cv.getStructuringElement(cv.MORPH_RECT, (size, size)), borderType = border)
    NewImageWindow(self.root, img_morph).show_image()
    nw.destroy

  def skeletonization(self):
    img = self.root.active_window.image.cv_img
    skel = np.zeros(img.shape, np.uint8)
    im_copy = img.copy()
    element = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))

    while True:
      im_open = cv.morphologyEx(im_copy, cv.MORPH_OPEN, element)
      im_temp = cv.subtract(im_copy, im_open)
      im_eroded = cv.erode(im_copy, element)
      skel = cv.bitwise_or(skel,im_temp)
      im_copy = im_eroded.copy()                                             
      if cv.countNonZero(im_copy)==0:
        break

    NewImageWindow(self.root, skel).show_image()

  def watershed(self):
    image = self.root.active_window.image.cv_img

    img_gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    
    _,thresh = cv.threshold(img_gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 1)
    sure_bg = cv.dilate(opening,kernel,iterations=1)
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
    _, sure_fg = cv.threshold(dist_transform,0.5*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg,sure_fg)
    _, markers = cv.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0
    markers2 = cv.watershed(image, markers)
    img_gray[markers2 == -1] = 255
    image[markers2 == -1] = [255,0,0]
    new_image = cv.applyColorMap(np.uint8(markers2*10), cv.COLORMAP_JET)
    NewImageWindow(self.root, new_image).show_image()

  def create_moments_table(self):
    img = self.root.active_window.image.cv_img

    nw = NewWindow(self.root)
    nw.resizable(False, False)
    nw.title('Moments table')

    moments = cv.moments(img)

    lst = [('moment', 'value')]

    for key in moments.keys():
      lst.append((key, moments[key]))
      self.draw_table(lst, nw)

  def create_object_feature_vector_table(self):
    img = self.root.active_window.image.cv_img

    _,thresh = cv.threshold(img,127,255,0) 
    contours,_ = cv.findContours(thresh, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE) 

    img3 = cv.cvtColor(thresh,cv.COLOR_GRAY2RGB)

    for cnt in contours:
      cv.drawContours(img3, [cnt], 0, (random.randrange(50,200,25),random.randrange(50,200,25),random.randrange(50,200,25)), 3)
  
    NewImageWindow(self.root, img3).show_image()

    nw = NewWindow(self.root)
    nw.resizable(False, False)
    nw.title('Object feature vector table')

    lst = [('contour', 'surface area', 'perimeter field', 'aspect ratio', 'extent', 'solidity',
            'equivalentDiameter ')]

    i = 1
    for contour in contours:
      area = cv.contourArea(contour)
      perimeter = cv.arcLength(contour,True)
      _,_,w,h = cv.boundingRect(contour)
      aspect_ratio = float(w)/h
      rect_area = w*h
      extent = float(area)/rect_area
      hull = cv.convexHull(contour)
      hull_area = cv.contourArea(hull)
      solidity = float(area)/hull_area
      equi_diameter = np.sqrt(4*area/np.pi)
      lst.append((i, area, perimeter, aspect_ratio, extent, solidity, equi_diameter))
      i = i + 1
    
    self.draw_table(lst, nw)

  def create_thresholding_window(self):
    window = self.root.active_window

    nw = NewWindow(self.root)
    Label(nw, text='thresholding level: ').grid(row=0, column=0)
    scale = Scale(nw, from_=0, to=255, orient=HORIZONTAL)
    scale.grid(row=0, column=1)
    button = Button(nw, text="Ok")
    button.grid(row=1, column=0) #TODO: co jezeli button nie ma configu
    scale.config(command= lambda value: self.thresholding(int(value), window, button, nw))


  def thresholding(self, thresh, window, button, nw): 
    _,img_th_binary = cv.threshold(window.image.cv_img, thresh, 255, cv.THRESH_BINARY)
    window.refresh_image(img_th_binary)
    button.config(command= lambda: window.save_new_image(img_th_binary, nw))

  def draw_table(self, lst, nw):
    for i in range(len(lst)):
      for j in range(len(lst[i])):
        entry = Entry(nw)
        entry.grid(row=i, column=j)
        entry.insert(END, lst[i][j])
        entry.config(state='disabled')

  def create_adaptive_thresholging_window(self):
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    
    Label(nw, text= "adaptive method: ").grid(row=0, column=0)
    methods = ['method1', 'method2']

    method = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=method)
    combobox1['values'] = methods
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    Label(nw, text= "threshold type: ").grid(row=1, column=0)
    types = ['type1', 'type2']

    type = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=type)
    combobox2['values'] = types
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    Label(nw, text='block size: ').grid(row=2, column=0)
    block = IntVar()
    Entry(nw, textvariable=block).grid(row=2, column=1)

    Button(nw, text='Ok', command=lambda: self.adaptive_thresholding(str(method.get()), str(type.get()), int(block.get()), img, nw)).grid(row=3, column=0)

  def adaptive_thresholding(self, method, type, block, img, nw):
    methods = {'method1' : cv.ADAPTIVE_THRESH_MEAN_C, 'method2' : cv.ADAPTIVE_THRESH_GAUSSIAN_C }
    method = methods[method]

    types = {'type1' : cv.THRESH_BINARY, 'type2' : cv.THRESH_BINARY_INV}
    type = types[type]
    
    img_th_adapt = cv.adaptiveThreshold(img, 255, method, type, block, 5)
    NewImageWindow(self.root, img_th_adapt).show_image()
    nw.destroy()

  def otsus_thresholding(self):
    img = self.root.active_window.image.cv_img
    blur = cv.GaussianBlur(img,(5,5),0)
    _,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    NewImageWindow(self.root, th3).show_image()

  def detect_lines_hough(self):
    img = self.root.active_window.image.cv_img
    color_img = cv.cvtColor(img, cv.COLOR_GRAY2RGB) #TODO: kolorowe się wywalają
    edges = cv.Canny(img, 50, 150, apertureSize=3)
    lines = cv.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is not None:
      for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv.line(color_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    NewImageWindow(self.root, color_img).show_image()

def diamond(size):
  return np.uint8(np.add.outer(*[np.r_[:size,size:-1:-1]]*2)>=size)

