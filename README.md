# API Backend for the parcel tracking app

## About the Project

This is a CRUD API for the parcel tracking. Additional functionality - getting weather for
the given postal code and country

### Built With

- Django
- Django Rest Framework
- PostgreSQL
- Redis

### Implemented features

- GET endpoint for the Articles
- GET endpoint for the Addreses
- Full CRUD for the user-shipments endpoint:
    - User with specific model permission can perform actions (GET, POST, PATCH, DELETE)
    - Owner (request.user == user) can get only his own shipments (readonly)
- Get weather for specific postal_code and country using [WeatherBit] ("https://www.weatherbit.io/")
    - Caching the responce using postal_code-country cache key, so requests to the same location would be returned from cache no more than every 2 hours
- token-based authentication using Djoser
- API schema using:
    - [Swagger] ("http://127.0.0.1:8000/api/schema/swagger-ui")
    - [Redoc] ("http://127.0.0.1:8000/api/schema/redoc/")
- Filter functionality on API calls
- Ability to expand, hide or display fields in API resp using query params
- Pytest coverage: **94.59%**
- Github Actions for testing, mypy and pylint checks, and deployment


### Prerequisites

List any prerequisites that are required to install the software.

- Docker and Docker Compose
- [Poetry] ("https://python-poetry.org/docs/#installation")
- [Pre-commit] ("https://pre-commit.com/#install")
- [Terraform] ("https://www.terraform.io/")  # only for AWS deployment


### Dev run
- install all dependencies using Poetry
    ```bash
    poetry install --no-root
    ```
- install pre-commit hooks
    ```bash
    pre-commit install
    ```
- copy .env.exapmle to .env
    ```bash
    cp .env.example .env
    ```
- adjust .env according your needs and security preferencies
    (if you want to use external database and redis - add required variables to the .env as well)
    (Dont forget to get your actual API key from [WeatherBit] ("https://www.weatherbit.io/"))
- activate Poetry shell
    ```bash
    poetry shell
    ```
- set django configuration name
    ```bash
    export DJANGO_CONFIGURATION=Dev
    ```
- start local docerized DB and Cache
    ```bash
    make start-local-db
    ```
- Apply all migrations
    ```bash
    python src/manage.py migrate
    ```
- Create superuser
    ```bash
    python src/manage.py createsuperuser
    ```
- Populate DB with dummy data
    ```bash
    python src/manage.py populate_shipment_data
    ```
- Run local server
    ```bash
    python src/manage.py runserver
    ```

### Deployment with AWS and Terraform (ECR + ECS + Fargate + RDS + Autoscaling + LB)
NB: the TF configuration presented here is a bit expensive for development, although it could handle quite a heavy load.

- Add terraform.tfvars file into the /terraform folder, and add there required variables (specify everything that does not have default value from /terraform/variables.tf)
- make sure you have all required AWS credentials installed in your local machine
- create S3 bucket to store terraform state and dynamoDB table to store state lock (you can use existing ones, or create your own. Make sure to match S3 and DynamoDB names with values in /terraform/main.tf)
- Init Terraform with "make terraform-init"
- Validate Terraform with "make terraform-validate"
- Plan Terraform with "make terraform-plan"
- Apply Terraform with "make terraform-apply"
- Destroy Terraform with "make terraform-destroy" (destroys everything)

- after applying TF, you could trigger "deploy" github action (you have to add secrets an env variables to the github before (see deploy.yml))
