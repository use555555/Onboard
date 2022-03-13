from OpenGL.GL import *
import numpy as np
from math import sin,cos,pi



class Circle:

    def __init__( self, circleData, totalSteps, resolution ):
        ''' circleData = Coordinate for points for creating Circle (x1, y1, x2, y2)
            totalSteps = Number of step used in vertices calculation
            resolution = Display Resolution (width, height)
            Out = Vertex data to use in shader
        '''

        self.vertices = ()
        self.vertexCount = totalSteps

        color = ( 1.0, 0.0, 0.0 )
        pixelX1 = circleData[ 0 ] * resolution[ 0 ]
        pixelY1 = circleData[ 1 ] * resolution[ 0 ]
        pixelX2 = circleData[ 2 ] * resolution[ 1 ]
        pixelY2 = circleData[ 3 ] * resolution[ 1 ]
        radius  = ( ( pixelX2 - pixelX1 )**2 + ( pixelY2 - pixelY1 )**2 )**0.5
        for step in range(0, totalSteps, 1):
            theta = ( 2*pi*step )/totalSteps
            posX = ( radius * cos( theta ) + pixelX1 ) / resolution[ 0 ]
            posY = ( radius * sin( theta ) + pixelY1 ) / resolution[ 1 ]
            self.vertices += ( posX, posY, 0.0 )
            self.vertices += color

        self.vertices = np.array( self.vertices, dtype=np.float32 )

        self.vao = glGenVertexArrays( 1 )
        glBindVertexArray( self.vao )

        self.vbo = glGenBuffers( 1 )
        glBindBuffer( GL_ARRAY_BUFFER, self.vbo )
        glBufferData( GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW )

        glEnableVertexAttribArray( 0 )
        glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 0 ) )

        glEnableVertexAttribArray(1)
        glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 12 ) )

    def destroy(self):
        glDeleteVertexArrays( 1, ( self.vao, ) )
        glDeleteBuffers( 1, ( self.vbo, ) )