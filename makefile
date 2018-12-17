.PHONY: test

# Run unit tests and then functional tests
test:
#	python3 -m pytest -m 'not functional' test
	python3 -m pytest -m 'functional' test
