SRC_PATH 		= sni
SPHINX_PATH 	= docs
RUN_ARGS	   ?=

SNI				= python3 -m sni -f test/sni.yml

.ONESHELL:

all: format typecheck lint

.PHONY: command-line-args
command-line-args:
	$(SNI) --help > $(SPHINX_PATH)/command-line-args.txt

.PHONY: docs
docs: docs_uml command-line-args  # openapi-spec
	sphinx-build -b html $(SPHINX_PATH)/ $(SPHINX_PATH)/_build
	-@xdg-open $(SPHINX_PATH)/_build/index.html

.PHONY: docs_uml
docs_uml:
	python -m plantuml docs/*.uml

.PHONY: openapi-spec
openapi-spec:
	$(SNI) --print-openapi-spec > $(SPHINX_PATH)/openapi.yml

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
	$(SNI) $(RUN_ARGS)

.PHONY: run-in-container
run-in-container:
	-docker volume create sni-code
	docker run --rm														\
		--env "GIT_URL=https://github.com/altaris/seat-navy-issue.git"	\
		--env "PYTHON_MAIN_MODULE=sni -f /etc/sni/sni.yml"				\
		--volume "sni-code:/usr/src/app/"					 			\
		--volume "$$(pwd)/test/sni.yml:/etc/sni/sni.yml"				\
		altaris/pumba

.PHONY: stack-down
stack-down:
	sudo docker-compose -f test/docker-compose.yml -p sni-test down

.PHONY: stack-up
stack-up:
	sudo docker-compose -f test/docker-compose.yml -p sni-test up -d \
		--remove-orphans

.PHONY: typecheck
typecheck:
	mypy $(SRC_PATH)/*.py
