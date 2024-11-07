DC = docker compose
ENV = --env-file .env
APP_FILE = docker_compose.yaml

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up -d
