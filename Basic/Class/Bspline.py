from OpenGL.GL import *
import numpy as np


class Bspline:

    def __init__( self, pointsCoordinate, totalSteps, mode, degree ):
        ''' pointsCoordinate = Coordinate for points for creating Bspline line (x1, y1, x2, y2, ...)
            totalSteps       = Number of step used in vertices calculation
            mode             = For setting open(True) or close(False) loop
            degree           = Degree of the b-spline curve
            Out = Vertex data to use in shader
        '''

        self.vertices = ()

        # Find how many point in the given data and set how many vertex will be in this curve
        self.pointCount = len( pointsCoordinate )//2
        self.vertexCount = totalSteps
        color = ( 1.0, 0.0, 0.0 )

        # Set the data to the appropriate shape for calculation
        pointsArray = np.array( pointsCoordinate )
        pointsArray = np.reshape( pointsArray, ( ( np.shape( pointsArray )[ 0 ] // 2 ), 2 ) )
        pointsArray = np.transpose( pointsArray )

        # Create knot vector
        knotVectorAmount = self.pointCount + degree + 1
        knotVector = []
        if mode:
            for i in range( 0, degree, 1 ):
                knotVector.append( 0 )
            for i in range( 0, knotVectorAmount-(2*degree), 1 ):
                knotVector.append( i )
            for i in range( 0, degree, 1 ):
                knotVector.append( max( knotVector ) )
        else:
            for i in range( 0, knotVectorAmount, 1 ):
                knotVector.append( i )

        # Normalize knot vector
        knotVector[:] = [ x / max( knotVector ) for x in knotVector ]

        # Vertices calculation
        for step in range( 0, totalSteps, 1 ):
            t = step/totalSteps
            basisFunction = []
            # Creating initial basis function
            for i in range( 0, knotVectorAmount-1, 1 ):
                if knotVector[ i ]<= t < knotVector[ i+1 ]:
                    basisFunction.append( 1 )
                else:
                    basisFunction.append( 0 )
            finishedBasisFunction = []

            # Calculation for the basis function
            for sample in range(0, len( basisFunction )-degree, 1):
                basisCalculation = basisFunction[ sample:sample+degree+1 ]
                j = 1
                calculatedBasisFunction = []
                while j<degree+1:
                    for i in range( 0, len( basisCalculation ) - 1, 1 ):
                        knotIndex = i + sample
                        if knotVector[ knotIndex+j ] - knotVector[ knotIndex ] == 0:
                            frontCox = 0
                        else:
                            frontCox =  ( t - knotVector[ knotIndex ] )/( knotVector[ knotIndex+j ] - knotVector[ knotIndex ] )
                        if knotVector[ knotIndex+j+1 ] - knotVector[ knotIndex+1 ] == 0:
                            backCox = 0
                        else:
                            backCox =  ( knotVector[ knotIndex+j+1 ] - t )/( knotVector[ knotIndex+j+1 ] - knotVector[ knotIndex+1 ] )
                        calculatedBasisFunction.append( frontCox*basisCalculation[ i ] + backCox*basisCalculation[ i + 1 ] )
                    basisCalculation = calculatedBasisFunction
                    calculatedBasisFunction = []
                    j += 1
                finishedBasisFunction.append( basisCalculation[ 0 ] )
            # Find vertices from b-spline equation
            coordinate = pointsArray * finishedBasisFunction
            self.vertices += ( sum( coordinate[ 0 ] ), sum( coordinate[ 1 ] ), 0.0 )
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