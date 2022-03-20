import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from Bezier import Bezier
import pyrr
import numpy as np


class App:

    def __init__(self):
        # variable
        ################################################
        self.width = 640
        self.height = 480

        # Full window curve
        # self.coordinate = ( 0, 240,
        #                     320, 480,
        #                     320, 0,
        #                     640, 240 )

        # Half window curve
        self.coordinate = ( 160, 240,
                            320, 360,
                            320, 120,
                            480, 240 )

        self.resolution = 1000
        ################################################
        # initialize python
        pg.init()
        pg.display.set_mode((self.width, self.height), pg.OPENGL | pg.DOUBLEBUF)
        # initialize OpenGL
        self.clock = pg.time.Clock()
        glClearColor( 0.1, 0.2, 0.2, 1 )  # Color when clear

        # Enable alpha transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.create_shader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)  # Initialize shader

        # Creating projection matrix
        projectionTransform = pyrr.matrix44.create_orthogonal_projection_matrix( 0.0, self.width, 0.0, self.height, 0.1, 100, np.float32 )
        # Send the projection matrix to be use in shader
        glUniformMatrix4fv( glGetUniformLocation( self.shader, "projection" ), 1, GL_FALSE, projectionTransform )

        # Creating model matrix
        modelTransform = pyrr.matrix44.create_from_translation( pyrr.Vector3( [ 0.0, 0.0, -1.0 ] ) )
        # Send the model matrix to be use in shader
        glUniformMatrix4fv( glGetUniformLocation( self.shader, "model" ), 1, GL_FALSE, modelTransform )

        self.bezierStart = Bezier( self.coordinate, self.resolution )
        self.mainloop()

    # Create shader to run drawing
    # vertexshader run once per vertex responsible to set position on screen and do transformation
    # fragmentshader run once per pixel responsible for calculating the colour in the pixel
    def create_shader(self, vertex_filepath, fragment_filepath):

        # access file and get source code in txt
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        # Compile each shader
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        # compileShader(Source code, Flag to indicate what type of shader we are compiling)

        return shader

    def mainloop(self):
        running = True
        while running:
            # check event
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            # COLOR_BUFFER = Big array storing color value on the screen
            # Every pixel color in OpenGl is stored in 32 bit u_int

            # Draw shape
            glUseProgram(self.shader)
            glBindVertexArray(self.bezierStart.vao)

            # Draw data from array
            glDrawArrays(GL_LINE_STRIP, 0, self.bezierStart.vertexCount)
            # glDrawArrays(shape, initial point, number of point to draw)

            pg.display.flip()  # Update pygame

            # timing
            self.clock.tick(60)

        self.quit()

    def quit(self):
        self.bezierStart.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

if __name__ == "__main__":
    myApp = App()
