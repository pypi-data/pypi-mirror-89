#
# "$Id: testhelp.py 28 2003-07-16 20:00:27Z andreasheld $"
#
# Help test program for pyFLTK the Python bindings
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

# 
#  'main()' - Display the help GUI...
# 

# int				#  O - Exit status
# main(int  argc,			#  I - Number of command-line arguments
#      char *argv[])		#  I - Command-line arguments
# {


help = Fl_Help_Dialog()
help.load("HelpDialog.html")
help.show()

Fl.run()

# 
#  End of "$Id: testhelp.py 28 2003-07-16 20:00:27Z andreasheld $".
# 
