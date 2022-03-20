from fltk import *
import sys
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from Bezier import Bezier
import numpy as np
import pyrr


def callback(widget):
    if (widget == button):
        if windowGL.collectingData != 1:
            windowGL.collectingData = 1
        elif windowGL.collectingData != 0:
            windowGL.collectingData = 0
        print( windowGL.collectingData )

    if (widget == clearButton):
        windowGL.coordinate = ()
        windowGL.redraw()

class MyWindow(Fl_Gl_Window):
    def __init__( self, xpos, ypos, width, height, label ):
        Fl_Gl_Window.__init__( self, xpos, ypos, width, height, label )
        # Variables #########################################################

        self.width = width
        self.height = height
        self.coordinate = ()
        self.resolution = 1000
        self.collectingData = 0

        #####################################################################
    def draw(self):
        if len( self.coordinate ) >= 4:
            self.shader = self.createShader( "shaders/vertex.txt", "shaders/fragment.txt" )
            glUseProgram(self.shader)

            self.bezierStart = Bezier( self.coordinate, self.resolution )

            # Creating projection matrix
            projectionTransform = pyrr.matrix44.create_orthogonal_projection_matrix( 0.0, self.width, 0.0, self.height,
                                                                                    0.1, 100, np.float32 )
            # Send the projection matrix to be use in shader
            glUniformMatrix4fv( glGetUniformLocation( self.shader, "projection" ), 1, GL_FALSE, projectionTransform )

            # Creating model matrix
            modelTransform = pyrr.matrix44.create_from_translation( pyrr.Vector3( [ 0.0, 0.0, -1.0 ] ) )
            # Send the model matrix to be use in shader
            glUniformMatrix4fv( glGetUniformLocation( self.shader, "model" ), 1, GL_FALSE, modelTransform )

            # refresh screen
            glClear( GL_COLOR_BUFFER_BIT )
            # COLOR_BUFFER = Big array storing color value on the screen
            # Every pixel color in OpenGl is stored in 32 bit u_int

            # Draw shape
            glUseProgram( self.shader )
            glBindVertexArray( self.bezierStart.vao )

            # Draw data from array
            glDrawArrays( GL_LINE_STRIP, 0, self.bezierStart.vertexCount )
            # glDrawArrays(shape, initial point, number of point to draw)
        else:
            glClear( GL_COLOR_BUFFER_BIT )

        pass

    def handle(self, event):
        if event == FL_PUSH:
            if self.collectingData == 1:
                self.coordinate += ( Fl.event_x(), self.height - Fl.event_y() )
                print(self.coordinate)
                self.redraw()
            return 1
        else:
            return Fl_Gl_Window.handle(self, event)

    def createShader( self, vertexFilepath, fragmentFilepath ):
        with open( vertexFilepath, 'r' ) as f:
            vertex_src = f.readlines()

        with open( fragmentFilepath, 'r' ) as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        return shader


###### SetUp ######
window = Fl_Window(860,556)     ###Creating Windows
window.label("Height Estimator")        ###Name the Windows

windowGL = MyWindow( 220, 76, 640, 480, "GLWindow" )
#########################################################
box = Fl_Box( 0, 0, 860 ,76,"Curve Drawer Program")   ####Creating box (x,y,width,height)
box.box(FL_UP_BOX)   ### Draw box
box.labelsize(36)
box.labelfont(FL_BOLD+FL_ITALIC)
box.labeltype(FL_SHADOW_LABEL)
#########################################################
button = Fl_Button( 0, 76, 220, 40, "Draw" )   ###(x, y, width, height, "label")
button.type( FL_NORMAL_BUTTON ) ###Normal Button
button.color( FL_GREEN ) ### Set Color
button.color2( FL_DARK_GREEN)  ### Set Color
button.when( FL_WHEN_RELEASE )  ###Set the action
button.callback(callback)
#########################################################
clearButton = Fl_Button( 0, 116, 220, 40, "Clear" )   ###(x, y, width, height, "label")
clearButton.type( FL_NORMAL_BUTTON ) ###Normal Button
clearButton.color( FL_WHITE ) ### Set Color
clearButton.color2( FL_GRAY)  ### Set Color
clearButton.when( FL_WHEN_RELEASE )  ###Set the action
clearButton.callback(callback)
#########################################################
Fl.event_button()
#########################################################
window.end()   ### ปิดหน้าต่างเก่า
window.show( sys.argv )  ### เเสดงผลหน้าต่างใหม่
#########################################################
Fl.run()  ###run the program
