PROJECT=cloudbenchmarksorg

PYHOME=.venv/bin
NOSE=$(PYHOME)/nosetests
FLAKE8=$(PYHOME)/flake8
PYTHON=$(PYHOME)/python


all: test

clean:
	rm -rf MANIFEST dist/* $(PROJECT).egg-info .coverage
	find . -name '*.pyc' -delete
	rm -rf .venv

test: .venv
	@echo Starting tests...
	tox

.venv:
	sudo apt-get install -qy python-virtualenv libpq-dev python-dev
	virtualenv .venv
	$(PYTHON) setup.py develop

serve: .venv
	.venv/bin/pserve development.ini

.PHONY: clean
