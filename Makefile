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
	uv export --no-hashes > requirements.txt
	npm -C ui upgrade
	wget -P ui https://github.com/saadeghi/daisyui/releases/latest/download/daisyui-theme.js

css:
	npx -C ui @tailwindcss/cli --minify -i ui/app.css -o config/static/uk-retejo.css

tailwind:
	npx -C ui @tailwindcss/cli --watch -i ui/app.css -o config/static/uk-retejo.css

admin:
	$(django) createsuperuser

migrations:
	$(django) makemigrations

migrate:
	$(django) migrate

attach:
	$(dc) attach django

pdb: attach
