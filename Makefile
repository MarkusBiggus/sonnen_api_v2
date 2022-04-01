CORE=sonnen_api_v2
TESTS=tests

PYTHON=python
PIP=pip


test:
	$(PYTHON) -m pytest $(TESTS) -b

test-cov:
	$(PYTHON) -m pytest --cov=$(CORE) $(TESTS) -b

test-cov-html:
	$(PYTHON) -m pytest --cov=$(CORE) $(TESTS) --cov-report html