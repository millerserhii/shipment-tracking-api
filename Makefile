

terraform-init:
	@cd terraform && terraform init

terraform-destroy:
	@cd terraform && terraform destroy -auto-approve

terraform-validate:
	@cd terraform && terraform validate

terraform-apply:
	@cd terraform && terraform apply -auto-approve

terraform-plan:
	@cd terraform && terraform plan

build-run:
	@export $(shell cat .env | xargs)
	@docker build -t $(ECR_REPOSITORY) --build-arg PORT=$(APP_CONTAINER_PORT) .
	@docker run -p $(APP_HOST_PORT):$(APP_CONTAINER_PORT) $(ECR_REPOSITORY)

start-local-db:
	@export $(shell cat .env | xargs)
	@docker compose -f compose.dev.yml up -d --build

stop-local-db:
	@docker compose -f compose.dev.yml down
