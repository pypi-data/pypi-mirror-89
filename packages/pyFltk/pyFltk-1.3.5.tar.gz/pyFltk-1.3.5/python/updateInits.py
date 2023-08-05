# this file defines the commands for updating the init
# methods (constructors) of the widget classes for pyFLTK
# run this before issuing the SWIG command


# where the actual command lines are stored
in_file = "initCommand.py"

# where the output is placed
out_file = "../swig/pyInit.i"


# file handlers
ofl = open(out_file, 'w')

def mapInit_Old(name, owns, virtual):
    # constructor
    line1 = "_swig_setattr(self, %s, 'this', apply(_fltk.new_%s, args))" % (name, name)
    line2 = "_swig_setattr(self, %s, 'thisown', %d)" % (name, owns)
    # only for virtual classes
    if virtual != 0:
        line3 = "self.registerSelf(self)"

    # prepare the output
    ofl.write("# override the implementation of the %s wrapper\n" % name)
    ofl.write("def __%sInit(self,*args):\n" % name)
    ofl.write("    %s\n" % line1)
    ofl.write("    %s\n" % line2)
    if virtual != 0:
        ofl.write("    %s\n" % line3)
    ofl.write("%s.__init__ = __%sInit\n" % (name, name))
    ofl.write("# end of the %s wrapper\n\n" % name)

def mapInit(name, owns, virtual):
    lines = []
    # constructor
    # only for director classes
    if virtual == 2:
        lines.append("if self.__class__ == %s:"%name)
        lines.append("  args = (None,) + args")
        lines.append("else:")
        lines.append("  args = (self,) + args")
    lines.append("newobj = _fltk.new_%s(*args)"%name)
    lines.append("self.this = newobj.this")
    lines.append("self.thisown = %d"%owns)
    lines.append("del newobj.thisown")
    # only for virtual classes
    if virtual == 1:
        lines.append("self.registerSelf(self)")

    # prepare the output
    ofl.write("# override the implementation of the %s wrapper\n" % name)
    ofl.write("def __%sInit(self,*args):\n" % name)
    for line in lines:
        ofl.write("    %s\n" % line)
    ofl.write("%s.__init__ = __%sInit\n" % (name, name))
    ofl.write("# end of the %s wrapper\n\n" % name)


if __name__ == '__main__':
    # write the header information
    ofl.write("# This file is auto generated. Do not Edit!\n")
    ofl.write("\n")
    ofl.write("%pythoncode {\n")
    
    ifl = open(in_file, 'r')
    for line in ifl.readlines():
        exec(line)

    # write the footer
    ofl.write("}\n")
    ofl.close()
