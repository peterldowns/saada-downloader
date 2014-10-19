# Makefile

.PHONY: clean

default: venv/bin/activate
	. venv/bin/activate && ./download.py

venv venv/bin/activate: requirements.txt clean
	test -d venv || virtualenv venv --no-site-packages
	. venv/bin/activate && pip install -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete

