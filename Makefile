UV ?= uv
PYTHON ?= $(UV) run python

.PHONY: install html serve clean check-uv

check-uv:
	@command -v "$(UV)" >/dev/null 2>&1 || { \
		echo "uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/ or run make UV=/path/to/uv"; \
		exit 127; \
	}

install: check-uv
	$(UV) sync

html: check-uv
	$(PYTHON) tools/build.py

serve: html
	$(PYTHON) tools/build.py --serve

clean:
	rm -rf output content/_remote
