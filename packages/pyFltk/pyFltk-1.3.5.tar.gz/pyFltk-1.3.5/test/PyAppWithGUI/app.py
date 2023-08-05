import ForwardDeclarations
import gui
#from gui import *  # this doesn't work because it creates a local copy
                    # of the global vars in gui.py

from fltk import *
import sys

def theBrowserCallback( ptr ):
	print "selected:"+str(gui.theBrowser.text(gui.theBrowser.value()))

def theOKCallback(ptr):
	sys.exit()

def initializeForwardDeclarations():
	ForwardDeclarations.theBrowserCallback = theBrowserCallback
	ForwardDeclarations.theOKCallback = theOKCallback


##################################################################
initializeForwardDeclarations()

mainwin = gui.make_window()
mainwin.show(len(sys.argv), sys.argv)

gui.theBrowser.add("C")
gui.theBrowser.add("C++")
gui.theBrowser.add("Perl")
gui.theBrowser.add("Python")

Fl.run()

