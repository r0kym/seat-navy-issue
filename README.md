SeAT Navy Issue
===============

*not affiliated with the original [SeAT](https://github.com/eveseat/seat)*

[![Swagger](https://badgen.net/badge/openapi/3/red)](https://editor.swagger.io/?url=https://raw.githubusercontent.com/altaris/seat-navy-issue/master/docs/openapi.yml)
[![Documentation](https://badgen.net/badge/documentation/here/green)](https://altaris.github.io/seat-navy-issue/)
[![Maintainability](https://api.codeclimate.com/v1/badges/c96b3a343687b9a4a3fa/maintainability)](https://codeclimate.com/github/altaris/seat-navy-issue/maintainability)
![Python 3](https://badgen.net/badge/Python/3/blue)
[![MIT License](https://badgen.net/badge/license/MIT/blue)](https://choosealicense.com/licenses/mit/)

![Logo 256x256](res/logo.256.png)

*logo derived from the work of [Smashicons](https://smashicons.com/)*

SeAT Navy Issue is a simpler alternative to
[SeAT](https://github.com/eveseat/seat). In short, it is an EVE Online
community manager, in the form of a REST API. Its core functionalities include:

* managing corporations, alliances, and even coalitions;
* creating and managing custom groups;
* storing and refreshing ESI tokens; making queries against the ESI;
* a simplistic clearance system;
* a Discord and Teamspeak connector.

Note that this project is just a backend. For a nice web-based user interface,
check out [SNI-frontend](https://github.com/r0kym/SNI-frontend).

# Getting started

## Dependencies

* `python3.8`;
* `requirements.txt` for runtime dependencies;
* `requirements.dev.txt` for development dependencies.

Simply run
```sh
virtualenv venv -p python3.8
. ./venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

## Running

```sh
make run  # Default command line arguments are '--clear-jobs'
RUN_ARGS='--help' make run  # Custom command line arguments
```

## Documentation

Simply run
```sh
make docs
```
This will generate the HTML doc of the project, and the index file should be at
`out/docs/html/index.html`.


## Code quality

Don't forget to run
```sh
make
```
to format the code following [pep8](https://www.python.org/dev/peps/pep-0008/),
typecheck it using [mypy](http://mypy-lang.org/), and lint check it. Note that
the formatter [yapf](https://github.com/google/yapf) does not yet support
Python 3.8 (see [issue #772](https://github.com/google/yapf/issues/772)), so
please refrain from using the walrus operator.
