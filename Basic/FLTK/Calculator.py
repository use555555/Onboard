from fltk import *
import sys
import time

window = Fl_Window( 640, 480 )
window.color( FL_GRAY_RAMP )

Box = Fl_Box( 190, 20, 260, 100, "Calculator" )
Box.box( FL_DIAMOND_DOWN_BOX )
Box.labelsize( 36 )
Box.labelfont( FL_BOLD+FL_ITALIC )
Box.labeltype( FL_SHADOW_LABEL )

Answer = Fl_Box( 20, 160, 150, 50, "Answer" )
Answer.box( FL_UP_BOX )
Answer.labelsize( 20 )
Answer.labelfont( FL_BOLD+FL_ITALIC )
Answer.labeltype( FL_SHADOW_LABEL )

Output = Fl_Output( 190, 160, 430, 50 )
Output.textsize( 20 )

Num1 = Fl_Box( 20, 230, 150, 50, "First Number" )
Num1.box( FL_UP_BOX )
Num1.labelsize( 20 )
Num1.labelfont( FL_BOLD+FL_ITALIC )
Num1.labeltype( FL_SHADOW_LABEL )

Num2 = Fl_Box( 320, 230, 170, 50, "Second Number" )
Num2.box( FL_UP_BOX )
Num2.labelsize( 20 )
Num2.labelfont( FL_BOLD+FL_ITALIC )
Num2.labeltype( FL_SHADOW_LABEL )

Input1 = Fl_Input( 20, 300, 260, 50 )
Input1.textsize( 20 )
Input2 = Fl_Input( 320, 300, 260, 50 )
Input2.textsize( 20 )

PlusButton = Fl_Button(  360, 410, 50, 50, "+"  )
PlusButton.labelsize( 24 )
PlusButton.labelfont( FL_BOLD+FL_ITALIC )
PlusButton.labeltype( FL_SHADOW_LABEL )

MiusButton = Fl_Button(  430, 410, 50, 50, "-"  )
MiusButton.labelsize( 24 )
MiusButton.labelfont( FL_BOLD+FL_ITALIC )
MiusButton.labeltype( FL_SHADOW_LABEL )

MultiplyButton = Fl_Button(  500, 410, 50, 50, "*"  )
MultiplyButton.labelsize( 24 )
MultiplyButton.labelfont( FL_BOLD+FL_ITALIC )
MultiplyButton.labeltype( FL_SHADOW_LABEL )

DivideButton = Fl_Button(  570, 410, 50, 50, "/"  )
DivideButton.labelsize( 24 )
DivideButton.labelfont( FL_BOLD+FL_ITALIC )
DivideButton.labeltype( FL_SHADOW_LABEL )

window.end()
window.show( sys.argv )

TimeStamp = time.time()

while Fl.wait() > 0:
    if PlusButton.value():
        Num1 = "".join( Input1.value().split() )
        Num2 = "".join( Input2.value().split() )
        try:
            Output.value(str(float(Num1) + float(Num2)))
        except:
            Output.value("Please enter number only")
    elif MiusButton.value():
        Num1 = "".join( Input1.value().split() )
        Num2 = "".join( Input2.value().split() )
        try:
            Output.value( str( float( Num1 ) - float( Num2 ) ) )
        except:
            Output.value( "Please enter number only" )
    elif MultiplyButton.value():
        Num1 = "".join( Input1.value().split() )
        Num2 = "".join( Input2.value().split() )
        try:
            Output.value( str( float( Num1 ) * float( Num2 ) ) )
        except:
            Output.value( "Please enter number only" )
    elif DivideButton.value():
        Num1 = "".join( Input1.value().split() )
        Num2 = "".join( Input2.value().split() )
        try:
            if float( Num2 ) != 0:
                Output.value( str( float( Num1 ) / float( Num2 ) ) )
            else:
                Output.value("Denominator can not be 0")
        except:
            Output.value( "Please enter number only" )

    if time.time() - TimeStamp >= 1 / 30:
        window.redraw()
        TimeStamp = time.time()
    pass