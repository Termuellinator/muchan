include .env

ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
DB_BACK_UP_DIR := $(ROOT_DIR)/db_backup

dev-start:
	python manage.py runserver --settings=config.settings.dev

prod-start:
	python manage.py runserver --settings=config.settings.prod

dev-install:
	pip install -r requirements/dev.txt

dev-migrate:
	python manage.py migrate --settings=config.settings.dev

dev-makemigrations:
	python manage.py makemigrations --settings=config.settings.dev

dev-showmigrations:
	python manage.py showmigrations --settings=config.settings.dev

dev-sqlmigrate:
	python manage.py sqlmigrate $(app) $(m) --settings=config.settings.dev

dev-shell:
	python manage.py shell --settings=config.settings.dev

backup:
	pg_dump -U $(DB_USER) -d $(DB_NAME) -f $(DB_BACK_UP_DIR)/DB_backup_$$(date +"%Y-%m-%-d-%H-%M-%S").sql