#! /usr/bin/env python
#
# "$Id: fltk_threads.py 495 2013-03-30 09:39:45Z andreasheld $"
#
# Thread test script for pyFLTK, the Python bindings
# for the Fast Light Tool Kit (FLTK).
# Port of the game by Michael Sweet
# Copyright 2005-2006 by Michael Sweet.
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
import threading, sys, time

class MyThread(threading.Thread):
    DoRun = True
    def __init__(self,string):
        threading.Thread.__init__(self)
        self.string = string
    def run(self):
        while self.DoRun:
            time.sleep(0.1)
            sys.stdout.write(self.string)

class UserInterface:
    ThreadList = []
    id = 1
    def __init__(self):
        self.window = Fl_Window(128, 176, 158, 150)

        self.start = Fl_Button(25, 25, 85, 25, "Start")
        self.start.callback(self.newProcessCB)
        
        self.click = Fl_Button(25,55,85,28,'Click')
        self.click.callback(self.clickCB)
        
        self.window.end()
    def appRun(self):
        self.window.show()
        #Fl.run()
        while self.window.visible():
            Fl.check()
            time.sleep(0.1)

        for t in self.ThreadList:
            print("Joining ", t)
            t.DoRun = False
            t.join()
        
    #callbacks:
    def newProcessCB(self,widget):
        t = MyThread('Thread %d\n'%self.id)
        self.id += 1
        t.start()
        self.ThreadList.append(t)
         
    def clickCB(self,widget):
        fl_mt_message('Hi')
        #fl_alert('Hi')

app = UserInterface()
app.appRun()

