py := poetry run
package_dir := src
tests_dir := tests

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install package with dependencies
	poetry install --with dev,test,lint

.PHONY: lint
lint: ## Lint code with flake8, pylint, mypy
	$(py) flake8 $(package_dir) --exit-zero
	$(py) pylint $(package_dir) --exit-zero
	$(py) mypy $(package_dir) || true

.PHONY: test
test: ## Run tests
	$(py) pytest $(tests_dir)

.PHONY: run
run:  # Run app
	$(py) python -m $(package_dir)

.PHONY: up
up:  # Run app in docker container
	docker compose --profile api --profile grafana up --build -d

.PHONY: build
build:  # Build docker image
	docker compose build

.PHONY: migrate
migrate:  # Run migration for postgres database
	docker compose --profile migration up --build
