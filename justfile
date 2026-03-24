# Module for Django in the backend dir
mod dj 'backend'

dc := "docker compose"
dc_exec := dc + " exec django"
django := dc_exec + " ./manage.py"

default:
    @just --list

install: update create_secrets copy_dotenv dj::copy_django_env
    @echo ""
    @echo "Farite. Nun tajpu:"
    @echo "just run"

[parallel]
update: update-py update-tailwind pull
    just build

# Start the whole project in dev mode with Vue and Tailwind
run:
    {{ dc }} up --build postgres django vue tailwind

# Start the Django project in dev mode
django:
    {{ dc }} up --build postgres django

[working-directory: 'backend']
update-py:
    uv sync --upgrade

update-tailwind:
    npm -C style upgrade

css:
    npm -C style run build:css

tailwind:
    npm -C style run watch:css

vue:
    npm run --prefix uk-aligxilo build

fontawesome:
    mkdir -p backend/config/static/fontawesome/css
    cp style/node_modules/@fortawesome/fontawesome-free/css/all.min.css config/static/fontawesome/css/all.min.css
    cp -r style/node_modules/@fortawesome/fontawesome-free/webfonts config/static/fontawesome/

[group('django')]
superuser:
    {{ django }} createsuperuser

[group('django')]
migrations args: && dj::format
    {{ django }} makemigrations {{args}}

[group('django')]
migrate:
    {{ django }} migrate

[group('django')]
sh:
    {{ dc_exec }} ash

[group('django')]
shell:
    {{ django }} shell_plus

[group('django')]
urls:
    {{ django }} show_urls

[group('django')]
attach:
    {{ dc }} attach django

pull:
    @echo "Tiras Docker-prakopiojn, povas daŭri klk minutojn…"
    {{ dc }} pull

build:
    {{ dc }} build

copy_dotenv:
    #!/usr/bin/env python3
    from os import getegid, geteuid
    from pathlib import Path

    dotenv = Path(".env")
    if dotenv.exists():
        print(f"Dosiero {dotenv} jam ekzistas, ne estos kreite.")
        exit(0)

    REPLACEMENTS = {
        "USER_ID = 1000": f"USER_ID = {geteuid()}",
        "GROUP_ID = 1000": f"GROUP_ID = {getegid()}",
    }

    with open(".env.example") as envfile_ex, open(dotenv, "w") as envfile:
        for line in envfile_ex:
            for key, value in REPLACEMENTS.items():
                line = line.replace(key, value)
            envfile.write(line)

create_secrets:
    #!/usr/bin/env python3
    from pathlib import Path
    from secrets import token_urlsafe

    SECRETS_DIR = Path("containers/secrets")
    SECRETS_FILES = ["POSTGRES_PASSWORD"]

    for secret_file in (SECRETS_DIR / name for name in SECRETS_FILES):
        # Ne tuŝi se ekzistas kaj plenas
        if secret_file.exists():
            with open(secret_file) as f:
                if len(f.read()) > 1:
                    print(f"Dosiero {secret_file} jam ekzistas.")
                    continue
        with open(secret_file, "w") as s:
            s.write(token_urlsafe(40))
            print(f"Pasvorto skribite en {secret_file}")



