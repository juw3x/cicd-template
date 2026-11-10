.PHONY: install lint format test docker-build docker-run

install:
	pip install -r requirements-dev.txt

lint:
	ruff check . && ruff format --check .

format:
	ruff check --fix . && ruff format .

test:
	pytest --cov=app

docker-build:
	docker build -t cicd-template-app:local .

docker-run:
	docker run --rm -p 8000:8000 cicd-template-app:local
