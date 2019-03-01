
test:
	pytest -vv --pep8 --flakes nerus

int:
	pytest -vv --capture=no --int nerus

cov:
	pytest -vv nerus --cov nerus --cov-report term-missing
