#Module for Python / Django
mod py 'backend'
# 
# Module for CSS / Tailwind / DaisyUI
mod style

dc := "docker compose"
dc_exec := dc + " exec django"
django := dc_exec + " ./manage.py"
dump_file := "uk-retejo-dump.sql.gz"
fa_module := "style/node_modules/@fortawesome/fontawesome-free"
fa_static := "./backend/config/static/fontawesome"

default:
    @just --list

install: create_secrets apply_selinux copy_dotenv py::copy_dotenv load_prod_data dl_prod_uploads install-dependencies fontawesome build
    @printf "\nFarite. Nun tajpu:\n\njust run\n"

[parallel]
install-dependencies: py::install style::install install-uk-retejo

[parallel]
update: py::update style::update pull
    just build

# Start the whole project in dev mode with Vue and Tailwind
run:
    {{dc}} up -w --build postgres django vue tailwind

# Start the Django project in dev mode
django:
    {{dc}} up -w --build django


install-uk-retejo:
    npm -C uk-aligxilo install

fontawesome:
    mkdir -p {{fa_static}}/css
    cp {{fa_module}}/css/all.min.css {{fa_static}}/css/all.min.css
    cp -r {{fa_module}}/webfonts {{fa_static}}/

[group('django')]
superuser:
    {{django}} createsuperuser

[group('django')]
migrations args='': && py::format
    {{django}} makemigrations {{args}}

[group('django')]
migrate args='':
    {{django}} migrate {{args}}

[group('django')]
sh:
    {{dc_exec}} ash

[group('django')]
shell:
    {{django}} shell_plus

[group('django')]
dbshell:
    {{dc}} exec postgres psql -U uk uk

[group('django')]
urls:
    {{django}} show_urls

[group('django')]
attach:
    {{dc}} attach django

pull:
    @echo "Tiras Docker-prakopiojn, povas daŭri klk minutojn…"
    {{dc}} pull

build:
    {{dc}} build django

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

apply_selinux:
    command -v chcon >/dev/null 2>&1 && exec chcon -t container_file_t -R containers/secrets

load_prod_data:
    ssh ikso.net 'docker compose -f /srv/Arcane/data/projects/uk-retejo/compose.yaml exec postgres pg_dump -U uk uk | gzip > /tmp/{{dump_file}}'
    rsync -P ikso.net:/tmp/{{dump_file}} ./containers/volumes/postgresql/
    ssh ikso.net 'rm /tmp/{{dump_file}}'

# Download production upload files (images, documents)
dl_prod_uploads:
    rsync -Prhz ikso.net:/srv/projects/uk-retejo/assets/uploads ./containers/volumes/assets/
