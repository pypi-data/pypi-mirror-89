#
# "$Id: image.py 495 2013-03-30 09:39:45Z andreasheld $"
#
# Image test program for pyFLTK the Python bindings
# for the Fast Light Tool Kit (FLTK).
#
# FLTK copyright 1998-1999 by Bill Spitzak and others.
# pyFLTK copyright 2003 by Andreas Held and others.
#
# This library is free software you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA.
#
# Please report all bugs and problems to "pyfltk-user@lists.sourceforge.net".
#

from fltk import *
from math import *
import sys


width = 100
height = 100
image = []

def make_image():
  	#image = new uchar[4*width*height];
  	#uchar *p = image;
	p = image
	index = 0

	y = 0
	while y < height:
		dy = float(y)/(height-1)
		x = 0
		while x < width:
			dx = float(x)/(width-1)
			p.append(int(255*((1.0-dx)*(1.0-dy))))
			index = index+1
			p.append(int(255*((1.0-dx)*dy)))
			index = index+1
			p.append(int(255*(dx*dy)))
			index = index+1
			dx = dx-0.5
			dy = dy-0.5
			alpha = int(255*sqrt(dx*dx+dy*dy))
			if alpha < 255:
				p.append(alpha)
			else:
				p.append(255)
			index = index+1
			dy = dy+0.5
			x = x+1
		y = y+1
	print("make_image done")
	return None


#globals
leftb = None
rightb = None
topb = None
bottomb = None
insideb = None
overb = None
inactb = None
b = None
w = None

def button_cb(ptr):
  global b, w

  i = 0
  if leftb.value():
    i = i + FL_ALIGN_LEFT
  if rightb.value():
    i = i + FL_ALIGN_RIGHT
  if topb.value():
    i = i + FL_ALIGN_TOP
  if bottomb.value():
    i = i + FL_ALIGN_BOTTOM
  if insideb.value():
    i = i + FL_ALIGN_INSIDE
  if overb.value():
    i = i + FL_ALIGN_TEXT_OVER_IMAGE
  b.align(i)
  if inactb.value():
    b.deactivate()
  else:
    b.activate()
  w.redraw()


def make_window():
	
	global leftb, rightb, topb, bottomb, insideb, overb, inactb, w, b
	
	window = Fl_Window(400,400)
	w = window
	window.color(FL_WHITE)
	b = Fl_Button(140,160,120,120,"Image w/Alpha")

	rgb = None
	dergb = None

	make_image()
	rgb = Fl_RGB_Image(image, width, height,4)
	print(sys.getrefcount(rgb)-1)
	dergb = rgb.copy()
	print(sys.getrefcount(dergb)-1)
	dergb.inactive()

	b.image(rgb)
	b.deimage(dergb)

	leftb = Fl_Toggle_Button(25,50,50,25,"left")
	leftb.callback(button_cb)

	rightb = Fl_Toggle_Button(75,50,50,25,"right")
	rightb.callback(button_cb)

	topb = Fl_Toggle_Button(125,50,50,25,"top")
	topb.callback(button_cb)

	bottomb = Fl_Toggle_Button(175,50,50,25,"bottom");
	bottomb.callback(button_cb)

	insideb = Fl_Toggle_Button(225,50,50,25,"inside")
	insideb.callback(button_cb)

	overb = Fl_Toggle_Button(25,75,100,25,"text over")
	overb.callback(button_cb)

	inactb = Fl_Toggle_Button(125,75,100,25,"inactive")
	inactb.callback(button_cb)

	window.end()

	return window

window = make_window()

window.resizable(window)

window.show(len(sys.argv), sys.argv)
#window.show()
 
Fl.run()
