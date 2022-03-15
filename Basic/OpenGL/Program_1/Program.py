import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np


class App:

    def __init__(self):
        # variable
        ################################################
        self.width = 640
        self.height = 480
        ################################################

        # Shape
        ################################################
        # Triangle
        # self.vertices = (
        #     -0.5, -0.5,  0.0, 1.0, 0.0, 0.0, 0.25,
        #      0.5, -0.5,  0.0, 0.0, 1.0, 0.0, 0.5,
        #      0.0,  0.5,  0.0, 0.0, 0.0, 1.0, 1.0
        # )

        # Rectangle
        self.vertices = (
            -0.5, -0.5,  0.0, 1.0, 1.0, 1.0, 1.0,
             0.5, -0.5,  0.0, 1.0, 1.0, 1.0, 0.75,
             0.5,  0.5,  0.0, 1.0, 1.0, 1.0, 0.5,
            -0.5,  0.5,  0.0, 1.0, 1.0, 1.0, 0.25
        )

        ################################################

        # initialize python
        pg.init()
        pg.display.set_mode((self.width, self.height), pg.OPENGL | pg.DOUBLEBUF)
        # initialize OpenGL
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.2, 1)  # Color when clear
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        self.shader = self.create_shader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)  # Initialize shader
        self.polygon = Polygon(self.shader, self.vertices)
        self.mainloop()

    def create_shader(self, vertex_filepath, fragment_filepath):

        # access file and get source code in txt
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        # Compile each shader
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

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

            # Draw shape
            glUseProgram(self.shader)
            glBindVertexArray(self.polygon.vao)

            # Draw data from array
            glDrawArrays(GL_POLYGON, 0, self.polygon.vertex_count)

            pg.display.flip()  # Update pygame

            # timing
            self.clock.tick(60)

        self.quit()

    def quit(self):
        self.polygon.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Polygon:

    def __init__(self, shader, vertices):
        # x,y,z,r,g,b
        self.vertices = vertices

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = len(self.vertices) // 7

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 28, ctypes.c_void_p(0))
        # Color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 28, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == "__main__":
    myApp = App()
