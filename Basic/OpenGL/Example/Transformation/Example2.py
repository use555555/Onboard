import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr


class App:

    def __init__(self):
        # variable
        ################################################
        self.width = 640
        self.height = 480
        ################################################
        # initialize python
        pg.init()
        pg.display.set_mode((self.width, self.height), pg.OPENGL | pg.DOUBLEBUF)
        # initialize OpenGL
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.2, 1)  # Color when clear

        # Enable alpha transparency
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        # Enable depth render
        glEnable(GL_DEPTH_TEST)

        self.shader = self.create_shader("shaders/Exvertex.txt", "shaders/Exfragment.txt")
        glUseProgram(self.shader)  # Initialize shader

        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        # Sending 1 integer to uniform location and setting sampler to 0

        self.wood_texture = Material("gfx/wood.jpeg")  # Get texture
        self.cat_texture = Material("gfx/cat.png")  # Get texture

        self.cube_mesh = CubeMesh(self.shader)
        self.cube = Cube(
            position=[0, 0, -3],
            eulers=[0, 0, 0]
        )

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect= self.width / self.height,
            near=0.1, far=10, dtype=np.float32
        )
        # Creating a projection matrix use to transform for our perspective
        # create_perspective_projection(Half of vertical fov, screen aspect, near depth, far depth, data type)

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )
        # Send uniform 4x4 Matrix with float value
        # glUniformMatrix4fv(Location, Number of matrix, Transpose, Data)

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        # Get location in shader

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

            # update cube
            self.cube.eulers[2] += 0.25
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360
            # euler module in Pyrr is Pitch Roll Yaw Respectively

            # self.cube.position[0] += 0.01
            # if self.cube.position[0] > 1:
            #     self.cube.position[0] -= 2

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # COLOR_BUFFER = Big array storing color value on the screen
            # Every pixel color in OpenGl is stored in 32 bit u_int
            # DEPTH_BUFFER = Big array storing depth value on the screen

            # Draw shape
            glUseProgram(self.shader)
            self.wood_texture.use()  # Use the texture
            # self.cat_texture.use()  # Use the texture

            # Start with identity
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            """
                pitch: rotation around x axis
                roll:rotation around z axis
                yaw: rotation around y axis
            """

            # Multiply the transformation
            # Rotation
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers), dtype=np.float32
                )
            )
            # Translation
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(self.cube.position), dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform) # Upload the data

            glBindVertexArray(self.cube_mesh.vao)

            # Draw data from array
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)
            # glDrawArrays(shape, initial point, number of point to draw)

            pg.display.flip()  # Update pygame

            # timing
            self.clock.tick(60)

        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        self.wood_texture.destroy()
        self.cat_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class CubeMesh:

    def __init__(self, shader):
        # x,y,z,r,g,b
        self.vertices = (
            - 0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 0,
            0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1, 0,
            0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 1, 1,

            0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 1, 1,
            -0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,
            -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 0,

            -0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0, 0,
            0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,
            0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 1,

            0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 1,
            -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 0, 1,
            -0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0, 0,

            -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,
            -0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 1, 1,
            -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,

            -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,
            -0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0, 0,
            -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,

            0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,
            0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 1, 1,
            0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,

            0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,
            0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0, 0,
            0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,

            -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,
            0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1, 1,
            0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,

            0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,
            -0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0, 0,
            -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,

            -0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 0, 1,
            0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 1, 1,
            0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,

            0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1, 0,
            -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 0, 0,
            -0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 0, 1
        )  # OpenGL use normalize device coordinate

        self.vertices = np.array(self.vertices, dtype=np.float32)
        # Change the data type to the data type that graphic card can read

        self.vertex_count = len(self.vertices) // 8

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
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        # Color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        # Texture coordinate
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))

    # Use to Free the memory when exit
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
        # (self.vao,) wrap in a list type to tell the function what list to delete


class Material:
    def __init__(self, filepath):
        self.texture = glGenTextures(1)  # Generate texture and allocate space in memory
        glBindTexture(GL_TEXTURE_2D, self.texture)  # Bind the texture

        # set S,T coordinate
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # Use to set left-right of texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # Use to set top-bottom of texture
        # Wrapping mode
        # Clamp to edge: Not go beyond certain point
        # Repeat: Virtually repeat the texture

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)  # Set what to do when minifying picture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Set what to do when magnifying picture
        # Linear: Smooth texture
        # Nearest: down sample texture

        image = pg.image.load(filepath).convert_alpha()  # Load the image and convert picture for using in OpenGL
        image_width, image_height = image.get_rect().size  # Get picture size
        img_data = pg.image.tostring(image, 'RGBA')  # Get image data change to string for OpenGL
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        # glTexImage2D(Texture location, Mip-map level, Specify internal format of image, width, height, border color,
        # format of data, data type, image data)
        # Mip-map: Progressively down sample image to make smaller image
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):  # Enable texture
        # OpenGL can load more than 1 texture at once
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.texture)

    def destroy(self):  # Clean memory
        glDeleteTextures(1, (self.texture,))


class Cube:  # Hold Position of the cube

    def __init__(self, position, eulers):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
if __name__ == "__main__":
    myApp = App()
