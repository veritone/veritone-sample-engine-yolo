python_version := 3.6
src_dir := src

.PHONY: check
#check: pylint pep8 test

.PHONY: test
test: ve
	. ve/bin/activate && find test/unit -name test*.py | PYTHONPATH=. xargs -n 1 python3

.PHONY: clean
clean:
	rm -rf ve/

ve:
	virtualenv $@ --python=python$(python_version)
	. ./$@/bin/activate && pip$(python_version) install -r requirements.txt

repl:
	. ve/bin/activate && python

lintable := $(src_dir) test

.PHONY: pylint
pylint: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs pylint --rcfile ./.pylintrc -d missing-docstring

.PHONY: pep8
pep8: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs pep8 --max-line-length=100

.PHONY: run
run:
	python3 $(src_dir)/engine.py
