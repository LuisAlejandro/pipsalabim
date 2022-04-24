.PHONY: clean-pyc clean-build docs clean
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python3 -c "$$BROWSER_PYSCRIPT"

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test clean-docs

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-docs:
	rm -fr docs/_build

lint: start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim flake8 pipsalabim

test: start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim python3 -m unittest -v -f

test-all: start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim tox

coverage: start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim coverage run --source pipsalabim -m unittest -v -f
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim coverage report -m
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim coverage html
	$(BROWSER) htmlcov/index.html

docs:
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim make -C docs clean
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim make -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim watchmedo shell-command -p '*.rst' -c 'make -C docs html' -R -D .

release: clean start dist
	twine upload -s -i luis@luisalejandro.org dist/*

dist: clean start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim python3 -m build
	ls -l dist

install: clean start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim pip3 install .

image:
	@docker-compose -p pipsalabim -f docker-compose.yml build \
		--force-rm --pull

start:
	@docker-compose -p pipsalabim -f docker-compose.yml up \
		--remove-orphans -d

console: start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim bash

stop:
	@docker-compose -p pipsalabim -f docker-compose.yml stop

down:
	@docker-compose -p pipsalabim -f docker-compose.yml down \
		--remove-orphans

destroy:
	@docker-compose -p pipsalabim -f docker-compose.yml down \
		--rmi all --remove-orphans -v

virtualenv: start
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim python3 -m venv --clear --copies ./virtualenv
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim ./virtualenv/bin/pip install -U wheel setuptools
	@docker-compose -p pipsalabim -f docker-compose.yml exec \
		--user luisalejandro pipsalabim ./virtualenv/bin/pip install -r requirements.txt -r requirements-dev.txt
