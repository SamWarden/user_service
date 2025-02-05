package_dir := "src"

# Show help message
help:
    just -l

# Install package with dependencies
install:
	poetry install --with dev,test,lint

# Run pre-commit
lint:
	just _py pre-commit run --all-files

# Run tests
test *args:
    just _py pytest {{args}}

# Run app
run:
	$(py) python -m {{package_dir}}

# Run app in docker container
up:
	docker compose --profile api --profile grafana up --build -d

# Stop docker containers
down:
	docker compose --profile api --profile grafana down

# Build docker image
build:
	docker compose build

# Run migration for postgres database
migrate:
	docker compose --profile migration up --build

_py *args:
    poetry run {{args}}
