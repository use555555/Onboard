from fltk import *
import sys
import time

# Define window size
window = Fl_Window( 580, 280 )
WindowColor = 0
# Set the color of the window
window.color( WindowColor )
# Create box with "Hello, World" string
Box = Fl_Box( 20, 40, 260, 100, "Hello, World!" ) # FL_Box( x, y, width, height, label )

# Set the type of box and the size, font, and style of the label
Box.box( FL_DIAMOND_DOWN_BOX ) # Type of background box
Box.labelsize( 36 )
Box.labelfont( FL_BOLD+FL_ITALIC )
Box.labeltype( FL_SHADOW_LABEL ) # Cast shadow behind the label

Button = Fl_Button(  300, 40, 260, 100, "Time to dance"  )
Button.labelsize( 24 )
Button.labelfont( FL_BOLD+FL_ITALIC )
Button.labeltype( FL_SHADOW_LABEL )

Input = Fl_Input( 20, 160, 260, 100 )
Input.textsize( 30 )
Output = Fl_Output( 300, 160, 260, 100 )
Output.textsize( 30 )

TimeStamp = time.time()

# Show the window and enter the FLTK event loop
window.end()
window.show(sys.argv)
while Fl.check() > 0:
    if Button.value():
        if Input.value() == "Mom is here":
            if time.time() - TimeStamp >= 1/30:
                Output.value("Hide")
                window.redraw()
                TimeStamp = time.time()
        else:
            if WindowColor > 50:
                WindowColor = 0
            else:
                WindowColor += 1
            window.color(WindowColor)
            if time.time() - TimeStamp >= 1/30:
                Output.value("Let's Party")
                window.redraw()
                TimeStamp = time.time()
    pass