from fltk import *

def alarm_to(v):
    print("timeout#: {0}".format(v))
 
    
def rone_cb(wid, v):
    print("Remove one timeout")
    Fl.remove_timeout(alarm_to, v[3]) #removes 3s


def rall_cb(wid):
    print("Remove all timeouts")
    Fl.remove_timeout(alarm_to)



w=Fl_Window(400,50, 200,200)
w.begin()
rall=Fl_Button(20,20,100,30,"Remove all")
rone=Fl_Button(20,70,100,30,"Remove one")
w.end()

val = (0,1,2,3,3,4)  #val *must* be immutable, cannot be a list
rall.callback(rall_cb)
rone.callback(rone_cb,val)
for x in range(len(val)):
    Fl.add_timeout(1.0+x, alarm_to, val[x])

w.show()
Fl.run()
