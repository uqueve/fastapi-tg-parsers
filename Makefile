DC = docker compose
LOGS = docker logs
ENV = --env-file .env

API_CONTAINER = euronews.fastapi
APP_FILE = docker_compose/api.yaml

MONGO_CONTAINER = euronews.mongodb
MONGO_FILE = docker_compose/mongo.yml


.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-build
app-build:
	${DC} -f ${APP_FILE} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${API_CONTAINER} -f

.PHONY: app-shell
app-shell:
	docker exec -it ${API_CONTAINER} bash

.PHONY: mongo
mongo:
	${DC} -f ${MONGO_FILE} ${ENV} up --build -d

.PHONY: mongo-down
mongo-down:
	${DC} -f ${MONGO_FILE} down

.PHONY: mongo-logs
mongo-logs:
	${LOGS} ${MONGO_CONTAINER} -f

.PHONY: mongo-shell
mongo-shell:
	docker exec -it ${MONGO_CONTAINER} bash
