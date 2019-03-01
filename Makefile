
test:
	pytest -vv --pep8 --flakes nerus

int:
	pytest -vv --capture=no --int nerus

cov:
	pytest -vv nerus --cov nerus --cov-report term-missing

clean:
	find nerus -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info coverage.xml
