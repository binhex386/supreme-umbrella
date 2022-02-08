SRC = supreme_umbrella/
IMAGE = supreme_umbrella

requirements.txt: poetry.lock
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: fmt
fmt:
	black $(SRC)
	isort $(SRC)

.PHONY: lint
lint:
	flake8 $(SRC)
	mypy --no-error-summary $(SRC)
	black --check --quiet $(SRC)
	isort --check --quiet $(SRC)

.PHONY: build
build:
	docker build -t $(IMAGE) .

.PHONY: run-local
run-local:
	docker-compose up -d db && \
	$(shell cat .env) \
	FLASK_APP=supreme_umbrella.main:app \
	FLASK_ENV=development \
	TEMPLATES_AUTO_RELOAD=True \
	flask run --reload

.PHONY: run-docker
run-docker:
	docker-compose up -d --build

.PHONY: init-docker
init-docker:
	docker-compose exec \
		-e FLASK_APP=supreme_umbrella.main:app \
		app \
		python -m flask init-db
