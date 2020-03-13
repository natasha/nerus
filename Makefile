
IMAGE = natasha/nerus-ctl

image:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

test:
	pytest -vv --pep8 --flakes nerus

int:
	pytest -vv --capture=no --int nerus --cov nerus --cov-report term-missing

ci:
	pytest -vv nerus/tests/test_api.py

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
		.coverage *.egg-info
