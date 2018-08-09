
DB_HOST = localhost
DB_NAME = buildings-db
DB_USER = buildings-user
DB_PASS = buildings-password

.PHONY: install
install:
	pip install buildings-api/

.PHONY: uninstall
uninstall:
	pip uninstall -y buildings-api

.PHONY: reinstall
reinstall: uninstall install

.PHONY: run
run:
	buildings-api buildings-api/settings.example.yml

# Quality of life helper for connecting to your database.
.PHONY: db-shell
db-shell:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME)

# Initializes the database with the schema only
.PHONY: db-init
db-init:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f sql/schema.sql

# Intializes the database with data. Assumes the schema has already been appied
.PHONY: db-load
db-load:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f sql/data.sql

# Drops the buildings table from the database if it exists
.PHONY: db-drop
db-drop:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f sql/revert.sql
