.PHONY: test unittests flaketest doctest

test: unittests flaketest doctest

unittests:
	coverage run -m unittest discover tests -v

flaketest:
	flake8 wsgi writer

doctest:
	sphinx-build -anW doc doc/_build/html
