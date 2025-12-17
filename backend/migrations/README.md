

# Database Migrations

Alembic is used for schema versioning.

## Setup

-The alembic package is installed by running ./start.sh 

-In a seperate terminal run docker compose exec backend bash. This opens a new bash terminal to run within the docker where alembic is installed

-Run the initial instruction [alembic upgrade head] in the bash terminal to format database to latest migration

### Create a migration

alembic revision --autogenerate -m "message"

### Migrate Forward

alembic upgrade head

### Migrate Backward

alembic downgrade -1

### Migrate to Earliest Version

alembic downgrade base

### Migrate to specific verison

alembic upgrade <version name>
