###############################################################################
# Common make values.
library   := ngdb
run       := pipenv run
python    := $(run) python
lint      := $(run) pylint
pyreverse := $(run) pyreverse
mypy      := $(run) mypy
coverage  := $(run) coverage
test      := $(coverage) run -m unittest discover -v -t $(shell pwd)

##############################################################################
# Setup/update packages the system requires.
.PHONY: setup
setup:				# Install all dependencies
	pipenv sync --dev

.PHONY: resetup
resetup:			# Recreate the virtual environment from scratch
	rm -rf $(shell pipenv --venv)
	pipenv sync --dev

.PHONY: depsoutdated
depsoutdated:			# Show a list of outdated dependencies
	pipenv update --outdated

.PHONY: depsupdate
depsupdate:			# Update all dependencies
	pipenv update --dev

.PHONY: depsshow
depsshow:			# Show the dependency graph
	pipenv graph

##############################################################################
# Checking/testing/linting/etc.
.PHONY: lint
lint:				# Run Pylint over the library
	$(lint) $(library) tests

.PHONY: test
test:				# Run unit tests
	$(test) tests

.PHONY: coverage
coverage:			# Show the current code coverage
	@$(coverage) report | awk '/^TOTAL/ { print "Coverage: " $$4 }'

.PHONY: coveragehtml		# Create a HTML report of the current code coverage
coveragehtml:
	$(coverage) html

.PHONY: coveragerep
coveragerep: coveragehtml       # Create and view a report of the current code coverage
	$(open_file) .coverage_report/index.html

.PHONY: coveragetxt
coveragetxt:			# Show a test-based code coverage report
	$(coverage) report

.PHONY: dscheck
dscheck:			# Perform a doc-string check
	pydscheck -e

.PHONY: typecheck
typecheck:			# Perform static type checks with mypy
	$(mypy) --scripts-are-modules $(library) tests $(wildcard examples/[a-z]*)

.PHONY: stricttypecheck
stricttypecheck:	        # Perform a strict static type checks with mypy
	$(mypy) --scripts-are-modules --strict $(library) tests $(wildcard examples/[a-z]*)

.PHONY: checkall
checkall: dscheck lint stricttypecheck test coverage # Check all the things

##############################################################################
# Utility.
.PHONY: repl
repl:				# Start a Python REPL
	$(python)

.PHONY: clean
clean:				# Clean the build directories
	rm -rf build dist $(library).egg-info

.PHONY: help
help:				# Display this help
	@grep -Eh "^[a-z]+:.+# " $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.+# "}; {printf "%-20s %s\n", $$1, $$2}'

##############################################################################
# Housekeeping tasks.
.PHONY: housekeeping
housekeeping:			# Perform some git housekeeping
	git fsck
	git gc --aggressive
	git remote update --prune

### Makefile ends here
