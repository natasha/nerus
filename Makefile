
test:
	flake8 nerus/__init__.py
	pytest -vv nerus/test.py
