.PHONY: test


test:
	python3 -m pytest test.py
	python3 -m unittest test_readme.py
