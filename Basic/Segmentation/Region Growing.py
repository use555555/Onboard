import numpy as np
from PIL import Image


# Object for point in the picture
class Point( object ):
    def __init__( self, x, y ):
        self.x = x
        self.y = y

    def getX( self ):
        return self.x

    def getY( self ):
        return self.y

# Calculating norm for it to be used in threshold comparing
def getGrayDiff( img, currentPoint, tmpPoint ):
    nowPoint = img.getpixel( ( currentPoint.x, currentPoint.y ) )
    nextPoint = img.getpixel( ( tmpPoint.x, tmpPoint.y ) )
    return ( ( ( nowPoint[ 0 ] - nextPoint[ 0 ] ) ** 2 ) + ( ( nowPoint[ 1 ] - nextPoint[ 1 ] ) ** 2 ) + ( ( nowPoint[ 2 ] - nextPoint[ 2 ] ) ** 2 ) ) ** 0.5

# Creating list that is used in finding neighboring points
def selectConnects(p):
    if p != 0:
        connects = [ Point( -1, -1 ), Point( 0, -1 ), Point( 1, -1 ), Point( 1, 0 ), Point( 1, 1 ),
                    Point( 0, 1 ), Point( -1, 1 ), Point( -1, 0 ) ]
    else:
        connects = [ Point( 0, -1 ), Point( 1, 0 ),Point( 0, 1 ), Point( -1, 0 ) ]
    return connects

# Do the region growing segmentation
def regionGrow( img, seeds, thresh, p = 1 ):
    width, height = img.size
    # Creating template image
    seedMark = np.zeros( ( height, width ) )
    seedList = []
    # Creating seed list to be use in region growing
    for seed in seeds:
        seedList.append( seed )
        label = 255
        connects = selectConnects( p )

    # Finding region
    while( len( seedList ) > 0 ):
        currentPoint = seedList.pop( 0 )

        seedMark[ currentPoint.y, currentPoint.x ] = label
        for i in range( len( connects ) ):
            tmpX = currentPoint.x + connects[ i ].x
            tmpY = currentPoint.y + connects[ i ].y
            if tmpX < 0 or tmpY < 0 or tmpX >= width or tmpY >= height:
                continue
            grayDiff = getGrayDiff( img, currentPoint, Point( tmpX, tmpY ))
            if grayDiff < thresh and seedMark[ tmpY, tmpX ] == 0:
                seedMark[ tmpY, tmpX ] = label
                seedList.append( Point( tmpX, tmpY ) )
    return seedMark


img = Image.open( 'test.png' )
seeds = [ Point( 110, 401 ), Point( 366, 159 ), Point( 712, 374 ) ]
binaryImg = regionGrow( img, seeds, 10, 1 )
img.show()
binary = Image.fromarray(binaryImg)
binary.show()
