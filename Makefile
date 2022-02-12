SRC = supreme_umbrella/
IMAGE = supreme_umbrella
ENV = \
	FLASK_APP=supreme_umbrella.main:app \
	FLASK_ENV=development \
	TEMPLATES_AUTO_RELOAD=True \
	$(shell cat .env)

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

.PHONY: start-db
start-db:
	docker-compose up -d db

.PHONY: debug-local
debug-local:
	$(ENV) flask run --reload

.PHONY: run-local
run-local:
	$(ENV) gunicorn -w 32 supreme_umbrella.main:app

.PHONY: run-docker
run-docker:
	docker-compose up -d --build

.PHONY: init-db
init-db:
	$(ENV) flask init-db

.PHONY: fill-db
fill-db:
	$(ENV) flask fill-db
