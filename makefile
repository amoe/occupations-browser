.PHONY: test


test:
	python3 -m pytest test_simple.py
	python3 -m unittest test_readme.py
