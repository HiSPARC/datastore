.PHONY: test unittests flaketest doctest devinstall

test: unittests flaketest doctest

unittests:
	coverage run -m unittest discover tests -v

flaketest:
	flake8 wsgi writer

doctest:
	sphinx-build -anW doc doc/_build/html

devinstall:
	conda install --yes --file requirements-conda.txt
	pip install -r requirements-dev.txt
