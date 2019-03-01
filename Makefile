
test:
	pytest -vv --pep8 --flakes nerus

cov:
	pytest -vv nerus --cov nerus --cov-report term-missing
