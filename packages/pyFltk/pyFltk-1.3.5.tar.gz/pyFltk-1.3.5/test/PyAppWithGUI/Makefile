PYFLTKDIR = ../..


all: links gui.py
	python app.py

.PHONY: gui.py
gui.py: gui.fl
	python $(PYFLTKDIR)/util/flconvert/flconvert gui.fl > gui.py


links: 
	rm -f fltk.py fltk_pre.py fltkc.so
	ln -s $(PYFLTKDIR)/python/fltk.py fltk.py
	ln -s $(PYFLTKDIR)/python/fltk_pre.py fltk_pre.py
	ln -s $(PYFLTKDIR)/python/fltkc.so fltkc.so

.PHONY: clean
clean:
	rm -f fltk.py fltk_pre.py fltkc.so *.pyc gui.py
	
