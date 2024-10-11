# Tested with GNU Make 3.8.1
MAKEFLAGS += --warn-undefined-variables
SHELL        	:= /usr/bin/env bash -e -u -o pipefail
.DEFAULT_GOAL := help
INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)

# cribbed from https://github.com/mozilla-services/telescope/blob/main/Makefile
.PHONY: help
help:  ## Prints out documentation for available commands
	@echo "Please use 'make <target>' where <target> is one of the following commands."
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)  ## Install dependencies
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [[ -z "$(POETRY)" ]]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	@echo "=> Installing python dependencies"
	"$(POETRY)" --version
	"$(POETRY)" install
	touch $(INSTALL_STAMP)

.PHONY: format-check
format-check: $(INSTALL_STAMP)  ## runs code formatting
	"$(POETRY)" run ruff format --check

.PHONY: format-fix
format-fix: $(INSTALL_STAMP)  ## runs code formatting
	"$(POETRY)" run ruff format

.PHONY: lint
lint: $(INSTALL_STAMP)  ## runs code formatting checks
	"$(POETRY)" run ruff check

.PHONY: lint-fix
lint-fix: $(INSTALL_STAMP)  ## runs code formatting checks
	"$(POETRY)" run ruff check --fix --exit-non-zero-on-fix

## Test
.PHONY: unit-test
unit-test: $(INSTALL_STAMP)  ## Run python unit tests
	"$(POETRY)" run pytest -v --cov --cov-report term --cov-report xml --cov-report html

.PHONY: test
test: unit-test format-check lint  ## Run unit tests, static analysis
	@echo "All tests passed."  # This should only be printed if all of the other targets succeed

.PHONY: check-dependencies
check-dependencies: $(INSTALL_STAMP)  ## check dependencies for vulnerabilities
	# 22 Aug 2024: 70612 vulnerability found with jinja2 version 3.1.4. At this time, all versions of jinja2 are affected, but vulnerability is being disputed. https://nvd.nist.gov/vuln/detail/CVE-2019-8341
	"$(POETRY)" run safety check -r poetry.lock --full-report -i 70612

.PHONY: clean
clean:  ## Delete any directories, files or logs that are auto-generated
	rm -rf results
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -f .install.stamp .coverage .coverage.*

.PHONY: deepclean
deepclean: clean  ## Runs cleans and deletes all poetry environments
	"$(POETRY)" env remove --all -n
	@echo Poetry environments deleted. Type 'exit' to exit the shell.
