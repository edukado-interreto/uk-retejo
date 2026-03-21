import os
from itertools import product
from pathlib import Path

from dj_database_url import parse as db_url_parse
from toml_decouple import TomlDecouple, config

from .embeds import EMBEDS_FINDERS
from .error_tracking import setup_bugsink
from .logging import PROD_LOGGING
from .utils import Environment, InternalIPs, django_vite_dev_mode

confi = TomlDecouple(prefix="UK_").load()

CONFIG_DIR = Path(__file__).parent
BASE_DIR = CONFIG_DIR.parent

SECRET_KEY: str = config("SECRET_KEY", "NESEKURA")
DEBUG = config("DEBUG", False)
ENVIRONMENT = Environment.init(config, DEBUG)

HOSTNAME = config("HOSTNAME", "127.0.0.1")
HOST = config("HOST", "0.0.0.0")
PORT = config("PORT", 8000)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", list({HOSTNAME, "localhost", "127.0.0.1", "0.0.0.0"})
)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", [f"https://{h}" for h in ALLOWED_HOSTS]
)


INSTALLED_APPS = [
    "debug_toolbar",
    "django_extensions",
    "django_rsgi",
    "django_vite",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    # "wagtail.images",
    "apps.base.apps.WagtailImagesAppConfig",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtailmenus",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.base",
    "apps.home",
    "apps.program",
    "apps.registration",
    "apps.search",
    "apps.site_settings",
]

if DEBUG:
    INSTALLED_APPS += ["apps.devel"]
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "devel_cache",
        }
    }

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    INTERNAL_IPS = InternalIPs()

# CORS headers for Vite dev mode
#
if DEBUG:
    INSTALLED_APPS = ["corsheaders", *INSTALLED_APPS]
    MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]
    CORS_ALLOWED_ORIGINS = [
        f"http{secure}://{host}:5173"
        for secure, host in product(("", "s"), ALLOWED_HOSTS)
    ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [CONFIG_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

if "DATABASE_URL" in config:
    DATABASES = {
        "default": {
            **config("DATABASE_URL", to=db_url_parse),
            "PASSWORD": config("POSTGRES_PASSWORD"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{cls}"}
    for cls in [
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    ]
]


# Internationalization

LANGUAGE_CODE = "eo"
TIME_ZONE = "Europe/Prague"
FORMAT_MODULE_PATH = ["config.formats"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = [CONFIG_DIR / "static"]
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "../assets/static"

MEDIA_URL = "/uploads/"
MEDIA_ROOT = BASE_DIR / "../assets/uploads"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

# Django sets a maximum of 1000 fields per form by default, but particularly complex
# page models can exceed this limit within Wagtail's page editor.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000


#### wAGTAIL SETTINGS ####

WAGTAIL_SITE_NAME = "Universala Kongreso"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = HOST

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.database"}}

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = "csv docx key odt pdf pptx rtf txt xlsx zip".split()
# https://docs.wagtail.org/en/stable/topics/writing_templates.html#responsive-embeds
WAGTAILEMBEDS_RESPONSIVE_HTML = True  # CSS class .responsive-object
WAGTAILEMBEDS_FINDERS = EMBEDS_FINDERS

# Wagtail Menus
WAGTAILMENUS_ACTIVE_CLASS = "menu-active"

# Ignoring these WARNINGS:
# wagtailmenus.FlatMenu: (wagtailadmin.W002) FlatMenu.content_panels will have
# no effect on snippets editing
# 	HINT: Ensure that FlatMenu uses `panels` instead of `content_panels` or
# 	set up an `edit_handler` if you want a tabbed editing interface.
# 	There are no default tabs on non-Page models so there will be no Content tab
# 	for the content_panels to render in.
SILENCED_SYSTEM_CHECKS = ["wagtailadmin.W002"]


# Vue / Vite integration
_VUE_STATIC_DIR = BASE_DIR / "apps/registration/static/vue"
DJANGO_VITE = {
    "default": {
        "manifest_path": _VUE_STATIC_DIR / "manifest.json",
        "static_url_prefix": "vue",
        "dev_mode": django_vite_dev_mode(DEBUG),
        "dev_server_host": config("HOST", HOST),
        "dev_server_port": "443",  # Overrides 5173
        "dev_server_protocol": "https",  # Overrides http
    }
}


if ENVIRONMENT.deployed:
    LOGGING = PROD_LOGGING
    setup_bugsink(config)
