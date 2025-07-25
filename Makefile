app := neaurlscript-automation

run:
	uv run fastapi dev

sync:
	uv sync

format:
	uv run ruff format

lint:
	uv run ruff check

link-fix:
	uv run ruff check --fix
