SRC_PATH 		= sni
SPHINX_PATH 	= docs
RUN_ARGS	   ?=

.ONESHELL:

all: format typecheck lint

.PHONY: clean
clean:
	sudo docker-compose -f test/docker-compose.yml -p sni-test down

.PHONY: docs
docs: docs_uml
	sphinx-build -b html $(SPHINX_PATH)/ $(SPHINX_PATH)/_build
	-@xdg-open $(SPHINX_PATH)/_build/html/index.html

.PHONY: docs_uml
docs_uml:
	python -m plantuml docs/*.uml

.PHONY: format
format:
	yapf --in-place --recursive --style pep8 --verbose $(SRC_PATH)

.PHONY: lint
lint:
	pylint $(SRC_PATH)

.PHONY: run
run:
	@set -a
	sudo docker-compose -f test/docker-compose.yml -p sni-test up -d --remove-orphans
	. ./venv/bin/activate
	python3 $(SRC_PATH)/sni.py $(RUN_ARGS)

.PHONY: typecheck
typecheck:
	mypy $(SRC_PATH)/*.py
