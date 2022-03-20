import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from Circle import Circle


class App:

    def __init__(self):
        # variable
        ################################################
        self.width = 640
        self.height = 480

        self.coordinate = (-0.5, 0.0, 0.0, 0.0 )

        self.resolution = 100
        ################################################
        # initialize python
        pg.init()
        pg.display.set_mode((self.width, self.height), pg.OPENGL | pg.DOUBLEBUF)
        # initialize OpenGL
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.2, 1)  # Color when clear

        # Enable alpha transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.create_shader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)  # Initialize shader

        self.Circle = Circle( self.coordinate, self.resolution, ( self.width, self.height ) )
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
            glBindVertexArray(self.Circle.vao)

            # Draw data from array
            glDrawArrays(GL_LINE_LOOP, 0, self.Circle.vertexCount)
            # glDrawArrays(shape, initial point, number of point to draw)

            pg.display.flip()  # Update pygame

            # timing
            self.clock.tick(60)

        self.quit()

    def quit(self):
        self.Circle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

if __name__ == "__main__":
    myApp = App()
