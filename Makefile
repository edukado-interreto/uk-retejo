dc := docker compose
django := $(dc) exec django ./manage.py

all: run

run:
	$(dc) up --build

install:
	mkdir -p assets/media assets/static .docker/postgres_data secrets
	head /dev/urandom | tr -dc A-Za-z0-9 | head -c 64 > secrets/postgres-password
	npm -C ui install

update:
	uv lock --upgrade
	./minimal-uv-pyproject -o .docker/pyproject.toml
	npm -C ui upgrade
	rm ui/daisyui-theme.js
	wget -P ui https://github.com/saadeghi/daisyui/releases/latest/download/daisyui-theme.js

css:
	npm -C ui run build:css

tailwind:
	npm -C ui run watch:css

admin:
	$(django) createsuperuser

migrations:
	$(django) makemigrations

migrate:
	$(django) migrate

attach:
	$(dc) attach django

pdb: attach
