import numpy as np

Coordinate = ( -0.5, 0.0,
               -0.25, 0.5,
               0.25, -0.5,
               0.5, 0 )

CoordinateArray = np.array( Coordinate )
# print( np.shape( CoordinateArray ) )
CoordinateArray = np.reshape( CoordinateArray,( ( np.shape( CoordinateArray )[ 0 ]//2 ), 2 ) )
# print( CoordinateArray *  2)
PointBefore = np.delete( CoordinateArray, -1, axis=0 )
PointAfter = np.delete( CoordinateArray, 0, axis=0 )
# print(PointBefore)
# print(PointAfter)

x = (1 - 0.5) * PointBefore + 0.5 * PointAfter
PointBefore = np.delete( x, -1, axis=0 )
PointAfter = np.delete( x, 0, axis=0 )

x = (1 - 0.5) * PointBefore + 0.5 * PointAfter

PointBefore = np.delete( x, -1, axis=0 )
PointAfter = np.delete( x, 0, axis=0 )

x = (1 - 0.5) * PointBefore + 0.5 * PointAfter

print(x[0][0])