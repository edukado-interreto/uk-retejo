#!/usr/bin/env python3
import subprocess
from os import getegid, geteuid
from pathlib import Path
from random import choices
from string import ascii_letters, digits

IGNORED_DIRS = [
    Path(f"./{name}")
    for name in ["secrets", ".docker/postgresql", "uploads/media"]
]
SECRETS_DIR = IGNORED_DIRS[0]
SECRETS_FILES = ["POSTGRES_PASSWORD_FILE"]


### LIBS ###


def load_dotenv(filename=".env") -> dict[str, str]:
    with open(Path(filename).resolve()) as env_file:
        return dict(
            line.strip().split(" = ")
            for line in env_file
            if line.strip() and not line.startswith("#")
        )


def make_password(lenth=64):
    return "".join(choices(ascii_letters + digits * 4, k=lenth))


### ACTIONS ###


def create_ignored_dirs():
    for directory in IGNORED_DIRS:
        directory.mkdir(mode=0o755, parents=True, exist_ok=True)


def copy_dotenv():
    dotenv, dotenv_example = Path(".env"), Path(".env.example")
    if dotenv.exists():
        print(f"Dosiero {dotenv} jam ekzistas, ni daŭrigu.")
        return

    REPLACEMENTS = {
        "USER_ID = 1000": f"USER_ID = {geteuid()}",
        "GROUP_ID = 1000": f"GROUP_ID = {getegid()}",
    }

    with open(dotenv_example) as envfile_ex, open(dotenv, "w") as envfile:
        for line in envfile_ex:
            for key, value in REPLACEMENTS.items():
                line = line.replace(key, value)
            envfile.write(line)


def copy_env_django():
    env_django, env_django_example = Path(".env.django"), Path(".env.django.example")
    if env_django.exists():
        print(f"Dosiero {env_django} jam ekzistas, ni daŭrigu.")
        return

    REPLACEMENTS = {"SECRET_KEY = NESEKURA": f"SECRET_KEY = {make_password()}"}

    with open(env_django_example) as dj_ex, open(env_django, "w") as dj:
        for line in dj_ex:
            for key, value in REPLACEMENTS.items():
                line = line.replace(key, value)
            dj.write(line)


def create_secrets():
    env = load_dotenv()

    for secret_file in (SECRETS_DIR / env[name] for name in SECRETS_FILES):
        # Ne tuŝi se ekzistas kaj plenas
        if secret_file.exists():
            with open(secret_file) as f:
                if len(f.read()) > 1:
                    print(f"Dosiero {secret_file} jam ekzistas.")
                    continue
        with open(secret_file, "w") as s:
            s.write(make_password())
            print(f"Pasvorto skribite en {secret_file}")


def install_npm_packages():
    print("\nInstalas NPM dependaĵojn… (npm -C ui install)", end="")
    subprocess.run("npm -C ui install", shell=True, check=True)


def install_python_requirements():
    print("\nInstalas Pitonaj dependaĵojn… (uv sync)")
    try:
        res = subprocess.run("uv sync", shell=True, check=True, capture_output=True)
        if output := res.stderr:
            print(output.decode())
    except subprocess.CalledProcessError as err:
        if err.returncode == 2:
            return
        print(err.stderr.decode())


def run_docker_build():
    print("Tiras kaj kunmetads Docker-prakopiojn, povas daŭri klk minutojn…")
    subprocess.run("docker compose pull", shell=True, check=True)
    subprocess.run("docker compose build", shell=True, check=True)


### ENTRYPOINT ###


def install():
    create_ignored_dirs()
    copy_env_django()
    create_secrets()
    install_npm_packages()
    install_python_requirements()
    run_docker_build()


if __name__ == "__main__":
    try:
        install()
        print("\nNun tajpu `make` por lanĉi Docker Compose.")
    except KeyboardInterrupt:
        print("\nInstalado haltite.")
