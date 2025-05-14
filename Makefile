dc := docker compose
django := $(dc) exec django ./manage.py

all: run

run:
	$(dc) up --build

install: download-tailwind
	mkdir -p assets/media assets/static .docker/postgres_data secrets
	head /dev/urandom | tr -dc A-Za-z0-9 | head -c 64 > secrets/postgres-password

lock:
	uv export --no-hashes > requirements.txt

ui:
	./ui/tailwindcss --minify -i ui/input.css -o config/static/uk-retejo.css

watch-daisyui:
	./ui/tailwindcss --watch -i ui/input.css -o config/static/uk-retejo.css

update-daisyui:
	wget https://github.com/saadeghi/daisyui/releases/latest/download/daisyui.js
	wget https://github.com/saadeghi/daisyui/releases/latest/download/daisyui-theme.js

admin:
	$(django) createsuperuser

migrations:
	$(django) makemigrations

migrate:
	$(django) migrate

attach:
	$(dc) attach django

pdb: attach

download-tailwind:
	wget -O ui/tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
	chmod +x ui/tailwindcss
