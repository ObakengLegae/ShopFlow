DOCKER ?= sudo docker
TEST_PATH ?=

.PHONY: all run_database test stop_database

all: run_database test stop_database
run_database:
	@$(DOCKER) compose up -d

stop_database:
	@$(DOCKER) compose down

test:
	@sleep 2
	@python3 -m pytest tests/$(TEST_PATH) -v
	@sleep 1
