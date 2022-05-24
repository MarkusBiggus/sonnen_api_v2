CORE=sonnen_api_v2
TESTS=tests

PYTHON=python
PIP=pip


test:
	$(PYTHON) -m pytest $(TESTS)

test-cov:
	$(PYTHON) -m pytest --cov=$(CORE) $(TESTS)

test-cov-html:
	$(PYTHON) -m pytest --cov=$(CORE) $(TESTS) --cov-report html