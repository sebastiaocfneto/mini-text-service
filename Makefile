.PHONY: help up down logs test test-docker fmt lint

help:
	@echo "Targets:"
	@echo "  make up         - Build and run the service via docker compose"
	@echo "  make down       - Stop containers (and remove volumes)"
	@echo "  make logs       - Follow service logs"
	@echo "  make test       - Run tests locally (requires python + deps installed)"
	@echo "  make test-docker- Run tests inside the built image"

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	pytest -q

test-docker:
	docker build -t mini-text-service:test .
	docker run --rm mini-text-service:test pytest -q
