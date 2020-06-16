SRC_PATH 		= sni
SPHINX_PATH 	= docs
RUN_ARGS	   ?=

.ONESHELL:

all: format typecheck lint

.PHONY: docs
docs:
	sphinx-build -b html $(SPHINX_PATH)/ $(SPHINX_PATH)/_build
	-@xdg-open $(SPHINX_PATH)/_build/html/index.html

.PHONY: format
format:
	yapf --in-place --recursive --style pep8 --verbose $(SRC_PATH)

.PHONY: lint
lint:
	pylint $(SRC_PATH)

.PHONY: run
run:
	@set -a
	-@. ./venv/bin/activate
	# -@. ./secret.env
	@python3 $(SRC_PATH)/sni.py $(RUN_ARGS)

.PHONY: typecheck
typecheck:
	mypy $(SRC_PATH)/*.py
