
install:
	pip install buildings-api/

uninstall:
	pip uninstall -y buildings-api

reinstall: uninstall install

run:
	buildings-api buildings-api/settings.example.yml

db-shell:
	PGPASSWORD=buildings-password psql -U buildings-user -h localhost -d buildings-db

db-init:
	PGPASSWORD=buildings-password psql -U buildings-user -h localhost -d buildings-db -f schema.sql

db-load:
	PGPASSWORD=buildings-password psql -U buildings-user -h localhost -d buildings-db -f data.sql
