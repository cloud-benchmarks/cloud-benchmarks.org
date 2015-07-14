PROJECT=cloudbenchmarksorg

PYHOME=.venv/bin
PYTHON=$(PYHOME)/python


all: test

clean:
	rm -rf $(PROJECT)/static/react/node_modules
	rm -rf MANIFEST dist/* $(PROJECT).egg-info .coverage
	find . -name '*.pyc' -delete
	rm -rf .venv

test: .venv
	@echo Starting tests...
	$(PYHOME)/tox

.venv:
	sudo apt-get install -qy python-virtualenv libpq-dev python-dev
	virtualenv .venv
	$(PYHOME)/pip install -U pip
	$(PYHOME)/pip install -e .

serve: .venv
	$(PYHOME)/initialize_db development.ini
	$(PYHOME)/pserve --reload development.ini

npm:
	cd $(PROJECT)/static/react; npm install

sample:
	@echo Posting sample submission...
	curl -X POST http://localhost:6542/submissions \
		-d @./tests/data/submission.json \
		--header "Content-Type: application/json"

.PHONY: clean
