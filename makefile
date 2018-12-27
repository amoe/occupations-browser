.PHONY: test

run_backend:
	FLASK_ENV=development flask run

# Run unit tests and then functional tests
test:
	python3 -m pytest -m 'not functional' test
	python3 -m pytest -m 'functional' test


install:
	rm -rf /usr/local/lib/occubrow
	cp -a . /usr/local/lib/occubrow
