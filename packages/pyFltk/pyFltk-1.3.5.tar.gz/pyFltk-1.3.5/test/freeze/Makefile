# Change this to point to your version of freeze
FREEZE = python /usr/doc/python-demos-1.5.2b1/Tools/freeze/freeze.py

# The rest should work without modification

all:	links output/hello

output/hello: output/hello.py
	$(FREEZE) -o output output/hello.py
	@echo Now changing to ./output
	cd output; make

output/hello.py: hello.fl
	python ../../util/flconvert/Code_py.py hello.fl > output/hello.py

output:
	mkdir output

clean:
	rm -rf fltkc.so fltk_pre.py fltk.py output

links: output
	rm -f fltkc.so fltk_pre.py fltk.py
	ln -s ../../python/fltkc.so .
	ln -s ../../python/fltk.py .
	ln -s ../../python/fltk_pre.py .
	rm -f output/fltkc.so 
	ln -s ../../../python/fltkc.so output/fltkc.so


