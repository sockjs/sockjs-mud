all:

clean:
	find mud -name \*.pyc |xargs --no-run-if-empty rm
