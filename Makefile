PROJECT=cloudbenchmarksorg

PYHOME=.venv/bin
PYTHON=$(PYHOME)/python


all: test

clean:
	rm -rf MANIFEST dist/* $(PROJECT).egg-info .coverage
	find . -name '*.pyc' -delete
	rm -rf .venv

test: .venv
	@echo Starting tests...
	$(PYHOME)/tox

.venv:
	sudo apt-get install -qy python-virtualenv libpq-dev python-dev
	virtualenv .venv
	$(PYTHON) setup.py develop

serve: .venv
	.venv/bin/pserve --reload development.ini

sample:
	@echo Posting sample submission...
	curl -X POST http://localhost:6543/submissions \
		-d @./tests/data/submission.json \
		--header "Content-Type: application/json"

.PHONY: clean
