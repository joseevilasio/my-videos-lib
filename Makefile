# Makefile
.PHONY: install update env set-app ipython clean test pflake8 fmt lint watch docs docs-serve build publish code-coverage

install:
	@poetry install

update:
	@poetry update

env:
	@poetry env use

set-app:
	@export FLASK_APP=api.app:create_app FLASK_ENV=development

test:
	@poetry run pytest -s --forked

code-coverage:
	@poetry run pytest --cov-report html --cov . 

coverage-report:
	@poetry run coverage report

citest:
	@poetry run py.test -v --cov-config .coveragerc --cov=api -l tests/ --junitxml=junit/test-results.xml
	@poetry run coverage xml
	make coverage-report

watch:
	#@poetry run ptw
	@ls **/*.py | entr pytest --forked

ipython:
	@poetry run ipython

lint:
	@poetry run pflake8

fmt:
	@poetry run isort api tests
	@poetry run black api tests

clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

docs:
	@mkdocs build --clean

docs-serve:
	@mkdocs serve

build:
	@poetry build

publish:
	@poetry publish
