# Define required macros here
SHELL = /bin/sh

SRCDIR = ./dependency_render
TESTDIR = ./tests

clean:
	python3 setup.py clean
	rm -rf build dist .coverage coverage.xml .eggs .scannerwork .pytest_cache *.egg-info $(SRCDIR)/__pycache__ $(TESTDIR)/__pycache__ MANIFEST

install: 
	python3 setup.py install

develop: 
	python3 setup.py develop

test-depend:
	python3 -m pip install coverage pytest pytest-runner requests_mock

test: test-depend
	python3 setup.py test

coverage: test-depend
	coverage run setup.py test
	coverage xml

coverage-html: coverage
	coverage html

sonar: coverage
	sonar-scanner -Dsonar.projectVersion=`python -c "import sys; from dependency_render import __version__; sys.stdout.write(__version__)"`

dist: 
	python3 setup.py sdist bdist_wheel

upload: dist
	python3 -m twine upload dist/*

check: dist
	python3 -m twine upload dist/*