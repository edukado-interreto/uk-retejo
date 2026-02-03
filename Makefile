dc := docker compose
django := $(dc) exec django ./manage.py

all: run

run:
	$(dc) up --build postgres django

install:
	./install.py

update: update-py update-js

update-py:
	uv lock --upgrade
	./minimal-uv-pyproject -o .docker/pyproject.toml pyproject.toml

update-js:
	npm -C ui upgrade

css:
	npm -C ui run build:css

tailwind:
	npm -C ui run watch:css

fontawesome:
	mkdir -p config/static/fontawesome/css
	cp ui/node_modules/@fortawesome/fontawesome-free/css/all.min.css config/static/fontawesome/css/all.min.css
	cp -r ui/node_modules/@fortawesome/fontawesome-free/webfonts config/static/fontawesome/

admin:
	$(django) createsuperuser

migrations:
	$(django) makemigrations
	uv run ruff format apps

migrate:
	$(django) migrate

shell:
	$(django) shell_plus

attach:
	$(dc) attach django

pdb: attach
