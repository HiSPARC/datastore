.PHONY: test unittests flaketest docstest gh-pages 

test: unittests flaketest doctest

unittests:
	coverage run -m unittest discover tests -v

flaketest:
	flake8 wsgi writer

doctest:
	sphinx-build -anW doc doc/_build/html

gh-pages:
ifeq ($(strip $(shell git status --porcelain | wc -l)), 0)
	git checkout gh-pages
	git rm -rf .
	git clean -dxf
	git checkout HEAD .nojekyll
	git checkout master doc writer wsgi examples
	make -C doc/ html
	mv -fv doc/_build/html/* .
	rm -rf doc/ writer/ wsgi/ examples/
	git add -A
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
	git checkout master
else
	$(error Working tree is not clean, please commit all changes.)
endif

