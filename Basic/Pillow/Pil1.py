from PIL import Image, ImageFilter
import os

size_300 = ( 300, 300 )
size_700 = ( 700, 700 )

# Get all file and save with resize
for f in os.listdir( '.' ):
    if f.endswith( '.jpeg' ):
        i = Image.open( f )
        fn, fext = os.path.splitext( f )

        i.thumbnail(size_700)
        i.save('700/{}_700{}'.format(fn, fext))

        i.thumbnail( size_300 )
        i.save( '300/{}_300{}'.format( fn, fext ) )

# Rotate picture
Me = Image.open( 'Me.jpeg' )
Me.rotate( 90 ).save( 'Mod/Me_rot.jpeg' )

# Convert to black and white
Me = Image.open( 'Me.jpeg' )
Me.convert( mode = 'L' ).save( 'Mod/Me_gray.jpeg' )

# Blur image
Me = Image.open( 'Me.jpeg' )
Me.filter( ImageFilter.GaussianBlur( 15 ) ).save( 'Mod/Me_blur.jpeg' )



