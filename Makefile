.PHONY: clean docs pypi

all: clean docs

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -fr dist/ *.egg-info/
	$(MAKE) -C docs clean

docs:
	$(MAKE) -C docs html

pypi:
	python setup.py register -r vivial
	python setup.py sdist upload -r vivial