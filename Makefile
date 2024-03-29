.PHONY: test
test: unittests linttest doctest

.PHONY: unittests
unittests:
	coverage run -m unittest discover tests -v
	coverage report

.PHONY: linttest
linttest:
	ruff check .
	ruff format --check .

.PHONY: doctest
doctest:
	sphinx-build -anW doc doc/_build/html

.PHONY: devinstall
devinstall:
	conda install --yes --file requirements-conda.txt
	pip install -r requirements-dev.txt
