DOCKER ?= sudo docker
PYTHON = python
TEST_PATH ?=

.PHONY: setup run_database stop_database test run_local tf_init tf_plan tf_apply tf_destroy

setup:
	$(PYTHON) -m pip install -r requirements.txt

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

tf_init:
	cd terraform && terraform init

tf_plan:
	cd terraform && terraform plan

tf_apply:
	cd terraform && terraform apply

tf_destroy:
	cd terraform && terraform destroy