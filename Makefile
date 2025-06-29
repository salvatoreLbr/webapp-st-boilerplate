.DEFAULT_GOAL := help
SHELL = bash


.PHONY: help
help: ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## install dependencies
	uv sync

.PHONY: test
test:
	uv run pytest --cov-report=term-missing --cov-report=xml --cov=src/webapp_st_boilerplate/ tests/test_webapp_st_boilerplate/
	uv run python scripts/generate_coverage_section.py

.PHONY: lint
lint:
	uv run ruff format src tests
	uv run ruff check --fix src tests

.PHONY: model-chart  ## sudo apt install graphviz
	dot -Tpng src/webapp_st_boilerplate/db/model.dot -o src/webapp_st_boilerplate/db/model.png
