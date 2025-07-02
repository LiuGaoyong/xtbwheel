#!/bin/bash

uv sync --active
rm -f dist/*whl
uv run --active python -m build --wheel
uv pip install dist/xtbwheel-*.whl
uv run --active pytest