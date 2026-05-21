UV ?= .local/bin/uv
PYTHON ?= $(UV) run python

.PHONY: install html serve clean

install:
	$(UV) sync

html:
	$(PYTHON) tools/build.py

serve: html
	$(PYTHON) tools/build.py --serve

clean:
	rm -rf output content/_remote
