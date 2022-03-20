from fltk import *

class MyWindow(Fl_Gl_Window):
  def __init__(self, xpos, ypos, width, height, label):
    Fl_Gl_Window.__init__(self, xpos, ypos, width, height, label)


App = MyWindow(100, 100,100,100,"HI")