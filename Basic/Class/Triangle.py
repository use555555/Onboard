from OpenGL.GL import *
import numpy as np


class Triangle:

    def __init__(self):
        # x,y,z,r,g,b
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
             0.0,  0.5, 0.0, 0.0, 0.0, 1.0
        )  # OpenGL use normalize device coordinate

        self.vertices = np.array(self.vertices, dtype=np.float32)
        # Change the data type to the data type that graphic card can read

        self.vertexCount = 3

        self.vao = glGenVertexArrays(1)  # Add attribute pointer to Vertex object to tell the meaning of the Vertex data
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)  # vertex buffer = Basic storage container
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)  # use to bind buffer
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        # Function that use to ship vertices to GPU
        # glBufferData(Where to load data, how many byte, data, how we plan to use)
        # Static_draw set data once use many times/ Dynamic_draw set and read data as much as you want

        # Describe how the attribute layout
        # glVertexAttribPointer(index, number of data, normalise number, stride from the data
        # each vertex have 6 number and each number have 4 bytes, offset in bytes)
        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

        # Color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


    # Use to Free the memory when exit
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
        # (self.vao,) wrap in a list type to tell the function what list to delete