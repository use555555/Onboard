from OpenGL.GL import *
import numpy as np


class Bezier:

    def __init__( self, pointsCoordinate, totalSteps ):
        ''' pointsCoordinate = Coordinate for points for creating Bezier line (x1, y1, x2, y2, ...)
            totalSteps   = Number of step used in vertices calculation
            Out = Vertex data to use in shader
        '''

        self.vertices = ()

        # Find how many point in the given data and set how many vertex will be in this curve
        self.pointCount = len( pointsCoordinate )//2
        self.vertexCount = totalSteps
        color = ( 1.0, 0.0, 0.0 )
        pointsArray = np.array( pointsCoordinate )
        pointsArray = np.reshape( pointsArray, ( ( np.shape( pointsArray )[ 0 ] // 2 ), 2 ) )

        for step in range( 0, totalSteps, 1 ):
            t = step/totalSteps

            # Set coordinate for this time step and calculate the interpolation time
            PointBefore = np.delete( pointsArray, -1, axis=0 )
            PointAfter = np.delete( pointsArray, 0, axis=0 )
            interpolationTimes = self.pointCount-1
            while interpolationTimes > 0:

                # Interpolation Calculation
                interpolatedPoints = ( 1 - t ) * PointBefore + t * PointAfter

                # Save data for the next iteration
                PointBefore = np.delete( interpolatedPoints, -1, axis=0 )
                PointAfter = np.delete( interpolatedPoints, 0, axis=0 )
                interpolationTimes -= 1

                # Set vertices from last iteration
                if interpolationTimes <= 0:
                    self.vertices += ( interpolatedPoints[ 0 ][ 0 ], interpolatedPoints[ 0 ][ 1 ], 0.0 )
                    self.vertices += color

        self.vertices = np.array( self.vertices, dtype=np.float32 )

        self.vao = glGenVertexArrays( 1 )
        glBindVertexArray( self.vao )

        self.vbo = glGenBuffers( 1 )
        glBindBuffer( GL_ARRAY_BUFFER, self.vbo )
        glBufferData( GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW )

        glEnableVertexAttribArray( 0 )
        glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 0 ) )

        glEnableVertexAttribArray( 1 )
        glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 12 ) )

    def destroy(self):
        glDeleteVertexArrays( 1, ( self.vao, ) )
        glDeleteBuffers( 1, ( self.vbo, ) )