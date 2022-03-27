from PIL import Image, ImageDraw, ImageFont

Me = Image.open( 'Me.jpeg' )
width, height = Me.size
print( width, height )

# Draw Line on picture
draw = ImageDraw.Draw( Me )
draw.line( ( width/2, 0, width/2, height ), fill = ( 255, 0, 0 ), width = 10 )
draw.line( ( 0, 0, width, height ), fill = ( 0, 255, 0 ), width = 30 )
# XXX.line( start and end coordinate, linecolor, line width )

Me.save( 'Draw/Me_draw.jpeg' )
Me.show()

Me = Image.open( 'Me.jpeg' )
width, height = Me.size
print( width, height )

# Draw shape in
draw = ImageDraw.Draw( Me )
draw.rectangle( ( width/2, 0, width, height/2 ), fill = ( 0, 0, 255 ), width = 50, outline = ( 255, 0, 0 ) )
# XXX.rectangle( top left and bottom right coordinate, fill color, border width, outline color )

draw.ellipse( ( width/2, height/2, width, height ), fill = ( 0, 0, 255 ), width = 50, outline = ( 0, 255, 0 ) )
# XXX.ellipse( top left and bottom right coordinate of bounding box, fill color, border width, outline color )


Me.save( 'Draw/Me_draw2.jpeg' )
Me.show()

Me = Image.open( 'Me.jpeg' )
width, height = Me.size
print( width, height )

# Draw text on picture
# Font
font = ImageFont.truetype( 'Font/zh-cn.ttf', 100 )
draw = ImageDraw.Draw( Me )
draw.text( ( 0, 0 ), 'Hello Everyone', fill = ( 0, 255, 0 ), font = font)
# XXX.text( top left coordinate, text, text color, font )

Me.save( 'Draw/Me_drawtext.jpeg' )
Me.show()

# Changing orientation using transpose
Me = Image.open( 'Me.jpeg' )
width, height = Me.size
print( width, height )

Rot = Me.transpose( Image.FLIP_TOP_BOTTOM )

Rot.save( 'Draw/Me_draw3.jpeg' )
Rot.show()