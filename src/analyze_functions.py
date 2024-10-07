import numpy as np
from validator import *
from view import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk
import random

class AnalyzeFunctions:
  def __init__(self, root):
    self.root = root

  def stretch_hist(self):
    if not Validator.validate_no_image(self.root):
      return 1

    if not Validator.validate_gray_image(self.root.active_window):
      return 1

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
    if not Validator.validate_no_image(self.root):
      return 1

    if not Validator.validate_gray_image(self.root.active_window):
      return 1

    img = self.root.active_window.image.cv_img
    cs = cumsum(get_img_value_array(self.root.active_window))
    cs_min = cs.min()
    cs_max = cs.max()
    cs = ((cs - cs_min) * 255 )/ (cs_max - cs_min)
    img_eq = cs[img]
    NewImageWindow(self.root, img_eq).show_image()

  def create_moments_table(self):
    if not Validator.validate_no_image(self.root):
      return 1
    img = self.root.active_window.image.cv_img
    if not Validator.validate_gray_image(self.root.active_window):
      return 1

    nw = NewWindow(self.root)
    nw.resizable(False, False)
    nw.title('Moments table')

    moments = cv.moments(img)

    lst = [('moment', 'value')]

    for key in moments.keys():
      lst.append((key, moments[key]))
      draw_table(lst, nw)

  def create_object_feature_vector_table(self):
    if not Validator.validate_no_image(self.root):
      return 1
    img = self.root.active_window.image.cv_img

    if not Validator.validate_gray_image(self.root.active_window):
      return 1

    _,thresh = cv.threshold(img,127,255,0) 
    contours,_ = cv.findContours(thresh, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE) 

    img3 = cv.cvtColor(thresh,cv.COLOR_GRAY2RGB)

    for cnt in contours:
      cv.drawContours(img3, [cnt], 0, (random.randrange(50,200,25),random.randrange(50,200,25),random.randrange(50,200,25)), 3)

    lst = [('contour', 'surface area', 'perimeter field', 'aspect ratio', 'extent', 'solidity',
            'equivalentDiameter ')]

    try:
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
      
      NewImageWindow(self.root, img3).show_image()

      nw = NewWindow(self.root)
      nw.resizable(False, False)
      nw.title('Object feature vector table')
      
      draw_table(lst, nw)
    except:
      messagebox.showerror("No objects", "No objects found")
      


  def create_selective_stretching_window(self):
    if not Validator.validate_no_image(self.root):
      return 1
    img = self.root.active_window.image.cv_img
    nw = NewWindow(self.root)
    p1 = IntVar()
    p2 = IntVar()
    q3 = IntVar()
    q4 = IntVar()
    ttk.Label(nw, text = "p1: ").grid(row=0, column=0)
    ttk.Entry(nw, textvariable=p1).grid(row=0, column=1)
    ttk.Label(nw, text= "p2: ").grid(row= 1, column=0)
    ttk.Entry(nw, textvariable=p2).grid(row=1, column=1)
    ttk.Label(nw, text= "q3: ").grid(row= 2, column=0)
    ttk.Entry(nw, textvariable=q3).grid(row=2, column=1)
    ttk.Label(nw, text= "q4: ").grid(row= 3, column=0)
    ttk.Entry(nw, textvariable=q4).grid(row=3, column=1)
    ttk.Button(nw, text= "Ok", command=lambda: self.selective_stretching(p1, p2, q3, q4, img, nw)).grid(row=4, column=1, sticky= W)

           
  def selective_stretching(self, p1, p2, q3, q4, img, nw):

    if Validator.validate_image_int_inputs(p1, p2, q3, q4):
      return 1
    
    p1 = int(p1.get())
    p2 = int(p2.get())
    q3 = int(q3.get())
    q4 = int(q4.get())

    if p1 > p2: p1, p2 = p2, p1
          
    img_stretched = img.copy()
    input_range = [p1, p2]
    output_range = [q3, q4]
    mask = (img_stretched >= input_range[0]) & (img_stretched <= input_range[1])
    img_stretched[mask] = (img_stretched[mask] - input_range[0]) * (output_range[1] - output_range[0]) / (
            input_range[1] - input_range[0]) + output_range[0]
    img_stretched = img_stretched.astype(np.uint8)

    NewImageWindow(self.root, img_stretched).show_image()
    nw.destroy()


  def show_bar_hist(self):
    if not Validator.validate_no_image(self.root):
      return 1
    
    my_hist = get_img_value_array(self.root.active_window)
    if my_hist is False:
      return 1
    
    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    plot.bar([str(x) for x in range(256)], my_hist)
    nw = NewWindow(self.root)
    canvas = FigureCanvasTkAgg(figure, master = nw)
    canvas.draw()
    canvas.get_tk_widget().pack()

  def watershed(self):
    if not Validator.validate_no_image(self.root):
      return 1
    image = self.root.active_window.image.cv_img

    if self.root.active_window.image.format == "RGB":
      img_gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    else:
      img_gray = image
      image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    
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
      

  def skeletonization(self):
    if not Validator.validate_no_image(self.root):
      return 1
    img = self.root.active_window.image.cv_img

    if not Validator.validate_gray_image(self.root.active_window):
      return 1

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
  

  def create_morphological_operations_window(self):
    if not Validator.validate_no_image(self.root):
      return 1
    img = self.root.active_window.image.cv_img

    nw = NewWindow(self.root)

    ttk.Label(nw, text= "Operation: ").grid(row=0, column=0)

    operation = StringVar()
    combobox1 = ttk.Combobox(nw, textvariable=operation)
    combobox1['values'] = ['erode', 'dilate', 'open', 'close']
    combobox1['state'] = 'readonly'
    combobox1.grid(row=0, column=1)

    ttk.Label(nw, text= "Shape: ").grid(row=1, column=0)

    shape = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=shape)
    combobox2['values'] = ['square', 'diamond']
    combobox2['state'] = 'readonly'
    combobox2.grid(row=1, column=1)

    ttk.Label(nw, text= "Size: ").grid(row=3, column=0)

    size = IntVar()
    ttk.Entry(nw, textvariable=size).grid(row=3, column=1)

    ttk.Label(nw, text= "Border: ").grid(row=4, column=0)

    border_type = StringVar()
    combobox2 = ttk.Combobox(nw, textvariable=border_type)
    combobox2['values'] = ['replicate', 'constant', 'reflect']
    combobox2['state'] = 'readonly'
    combobox2.grid(row=4, column=1)

    ttk.Button(nw, text= "Ok", command=lambda: 
      self.morphological_operations(operation, shape, size,
      border_type, img, nw)).grid(row=5, column=1, sticky= W)

  def morphological_operations(self, operation_str, shape_str, size, border_str, img, nw):

    if Validator.validate_combobox(operation_str, shape_str, border_str):
      return 1

    if Validator.validate_image_int_inputs(size) or Validator.validate_odd_number(size, "size"):
      return 1

    size = int(size.get())
    operation_str = str(operation_str.get())
    shape_str = str(shape.get())
    border_str = str(border_str.get())

    operation_dict = {'erode' : cv.MORPH_ERODE, 'dilate' : cv.MORPH_DILATE,
                      'open' : cv.MORPH_OPEN, 'close' : cv.MORPH_CLOSE}
    operation = operation_dict[operation_str]

    shape_dict = {'square' : cv.getStructuringElement(cv.MORPH_RECT, (size, size)),
                  'diamond' : diamond(size)}
    shape = shape_dict[shape_str]

    border_dict = {'replicate' : cv.BORDER_REPLICATE,
                  'constant' : cv.BORDER_CONSTANT,
                  'reflect' : cv.BORDER_REFLECT}
    border = border_dict[border_str]

    img_morph = cv.morphologyEx(img, operation, shape, borderType = border)
    NewImageWindow(self.root, img_morph).show_image()
    nw.destroy

  def detect_lines_hough(self):
    if not Validator.validate_no_image(self.root):
      return 1
    img = self.root.active_window.image.cv_img
    img2 = img.copy()
    if self.root.active_window.image.format != "RGB":
      color_img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    else: 
      color_img = img2
    edges = cv.Canny(img2, 50, 150, apertureSize=3)
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

# -------------------------------------

def diamond(size):
  return np.uint8(np.add.outer(*[np.r_[:size,size:-1:-1]]*2)>=size)

def cumsum(a):
  a = iter(a)
  b = [next(a)]
  for i in a:
      b.append(b[-1] + i)
  return np.array(b)

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

def draw_table(lst, nw):
    for i in range(len(lst)):
      for j in range(len(lst[i])):
        entry = ttk.Entry(nw)
        entry.grid(row=i, column=j)
        entry.insert(END, lst[i][j])
        entry.config(state='disabled')