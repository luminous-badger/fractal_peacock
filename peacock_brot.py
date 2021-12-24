#!/usr/bin/python3

# For 1, L, and I images, use integers. For RGB images, use a 3-tuple containing integer values. 
# For F images, use integer or floating point values.
# Basic Pillow Brot.
# JM Fri 16 Feb 2018 14:23:52 GMT
# So-called peacock. From: https://fractalfoundation.org/fractivities/FractalPacks-EducatorsGuide.pdf
# Z = Zold - ( Z^2 - 1 ) / a*(Z^2 + 1 )

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as nm
import cmath
from timeit import default_timer as timer
from lc import colour_list 

start = timer()

X_MIN = -20.5
X_MAX =  1.8
Y_MIN = -2.0
Y_MAX =  2.0
offset     = 0.01
maxiter    = 50
calc_count = 0
rnum       = 93
lenlc      = len( colour_list ) 
ZPower     = -2.0
A          = 1.7

# create a new X*Y pixel image surface
# make the background white (default bg=black)
X_SIZE = ( X_MAX - X_MIN ) / offset
Y_SIZE = ( Y_MAX - Y_MIN ) / offset

X_SIZE += 1
Y_SIZE += 1

X_SIZE = int( X_SIZE )
Y_SIZE = int( Y_SIZE )

print( 'X: ', X_SIZE ,' Y: ', Y_SIZE )

white      = (255,255,255)
randcolour =  (  190, 19, 19 )
blue       = ( 176,196,222 )
img        = Image.new( "RGB", [ X_SIZE, Y_SIZE ], white )

mycolour = ( 100, 150, 200 ) 
x_pixel = 0
for X in nm.arange ( X_MIN, X_MAX, offset ):
	y_pixel = 0
	for Y in nm.arange ( Y_MIN, Y_MAX, offset ):
		#Z = complex ( 0, 0 )
		Z = complex ( X, Y )
		iter_count = 0

		while ( abs ( Z**ZPower ) < 4 and iter_count < maxiter ):
			Z = Z - ( (Z**ZPower - 1 ) / A*( Z**ZPower + 1 ) )
			iter_count = iter_count + 1
			#print '{0:3d}'.format( iter_count ),
			calc_count = calc_count + 1  
                #mycolour = ( 13 * iter_count, 23 * iter_count, 33 * iter_count ) 
		if ( iter_count + rnum  >= lenlc ):
			mycolour = colour_list[ iter_count % lenlc ]
		else:   
			mycolour = colour_list[ iter_count + rnum  ]
		if ( iter_count <= 0 ):
			try:
				img.putpixel( ( x_pixel,  y_pixel ), white ) 
			except:
				print( 'Err: X,Y', x_pixel,  y_pixel)
				#pass
		elif ( iter_count == maxiter ):
			img.putpixel( ( x_pixel,  y_pixel ), white ) 
		else:
			img.putpixel( ( x_pixel,  y_pixel ), mycolour ) 
		y_pixel += 1

	x_pixel += 1

dt = timer() - start

MsgText = 'Peacock for Z^' + str( ZPower ) + ' X:' + str( X_MIN ) + str( X_MAX ) + ' ,Y:' + str( Y_MIN ) + str( Y_MAX ) + ' rnum:' + str( rnum ) + ' A: '+ str(A)

y_text_pos = y_pixel - 15
# ie, just above he bottom of the picture. In white part of pic.
fname = 'Peacock_Brot_X:' + str( X_MAX ) + str( X_MIN ) + '_Y:' + str( Y_MAX ) + str( Y_MIN ) + '.png'
print( 'Fname:', fname)

draw = ImageDraw.Draw(img)
font = ImageFont.truetype( "/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-B.ttf", 12 )
draw.text( ( 0, 0 ),  MsgText, ( 139,0,0 ), font=font )
#draw.text( ( 0, y_text_pos ),  MsgText, ( 139,0,0 ), font=font )

print( MsgText + ' created in %f s' % dt)
print( 'pixel:', x_pixel, y_pixel)
print( 'Calc: ', '{:,}'.format( calc_count ))

img.show( title=MsgText )
img.save( fname )

