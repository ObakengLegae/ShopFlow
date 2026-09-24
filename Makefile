DOCKER ?= sudo docker
PYTHON = python
TEST_PATH ?=

.PHONY: run_database stop_database test run_local

run_database:
	@$(DOCKER) compose up -d
	@sleep 2

stop_database:
	@$(DOCKER) compose down

test: run_database
	@python3 -m pytest tests/$(TEST_PATH) -v
	@$(MAKE) stop_database

run_local: run_database
	$(PYTHON) src/shopflow/pipeline.py

