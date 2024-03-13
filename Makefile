VERSION = 2.1.1

.PHONY: all clean test build

all: upload clean;

build:
	python setup.py sdist
	python setup.py bdist_wheel
	rm -rf build

upload: build
	twine upload dist/*${VERSION}*

install:
	pip install -e . --force-reinstall

test:
	python -m unittest discover -s tests

clean:
	rm -rf *.egg-info .pytest_cache build