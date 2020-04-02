
test:
	pytest \
		-vv --pep8 --flakes nerus \
		--cov nerus --cov-config setup.cfg \
		--cov-report term-missing --cov-report xml nerus

wheel:
	python setup.py bdist_wheel

version:
	bumpversion minor

upload:
	twine upload dist/*

clean:
	find . \
		-name '*.pyc' \
		-o -name __pycache__ \
		-o -name .DS_Store \
		| xargs rm -rf
	rm -rf dist/ build/ .pytest_cache/ .cache/ .ipynb_checkpoints/ \
		.coverage *.egg-info/
