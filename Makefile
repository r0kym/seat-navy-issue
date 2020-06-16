SRC_PATH 		= sni
SPHINX_PATH 	= docs
RUN_ARGS	   ?=

.ONESHELL:

all: format typecheck lint

.PHONY: docs
docs: docs_uml
	sphinx-build -b html $(SPHINX_PATH)/ $(SPHINX_PATH)/_build
	-@xdg-open $(SPHINX_PATH)/_build/html/index.html

.PHONY: docs_uml
docs_uml:
	python -m plantuml docs/*.uml

.PHONY: openapi-spec
openapi-spec:
	python3 $(SRC_PATH)/sni.py --openapi-spec > $(SPHINX_PATH)/openapi.yml

.PHONY: format
format:
	yapf --in-place --recursive --style pep8 --verbose $(SRC_PATH)

.PHONY: lint
lint:
	pylint $(SRC_PATH)

.PHONY: run
run:
	@set -a
	@. ./venv/bin/activate
	python3 $(SRC_PATH)/sni.py -f test/sni.yml $(RUN_ARGS)

.PHONY: stack-down
stack-down:
	sudo docker-compose -f test/docker-compose.yml -p sni-test down

.PHONY: stack-up
stack-up:
	sudo docker-compose -f test/docker-compose.yml -p sni-test up -d --remove-orphans

.PHONY: typecheck
typecheck:
	mypy $(SRC_PATH)/*.py
