DC = docker compose
LOGS = docker logs
API_CONTAINER = test_parsers.fastapi

hello:
	echo "hiii"

.PHONY: app
app:
	${DC} up -d

.PHONY: app-down
app-down:
	${DC} down

.PHONY: app-build
app-build:
	${DC} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${API_CONTAINER} -f

.PHONY: app-shell
app-shell:
	docker exec -it ${API_CONTAINER} bash