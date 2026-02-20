from itertools import product
from pathlib import Path

from toml_decouple import TomlDecouple
from .utils import django_vite_dev_mode, parse_db_url

config = TomlDecouple(prefix="UK_").load()

CONFIG_DIR = Path(__file__).parent
BASE_DIR = CONFIG_DIR.parent

SECRET_KEY = config.SECRET_KEY
DEBUG = config.DEBUG
HOST = config("HOST", default="http://localhost:8000")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", [HOST, "localhost", "127.0.0.1", "0.0.0.0"])
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=[f"https://{h}" for h in ALLOWED_HOSTS],
)

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "debug_toolbar",
    "django_extensions",
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


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

# CORS headers for Vite dev mode
if DEBUG:
    # INSTALLED_APPS = ["corsheaders", *INSTALLED_APPS]
    # MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]
    CORS_ALLOWED_ORIGINS = [
        f"http{secure}://{host}:5173"
        for secure, host in product(("", "s"), ALLOWED_HOSTS)
    ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            CONFIG_DIR / "templates",
        ],
        "APP_DIRS": True,
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

DATABASES = {
    "default": {
        **config("DATABASE_URL", to=parse_db_url),
        "PASSWORD": config("POSTGRES_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
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
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "uploads" / "media"
MEDIA_URL = "/media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
# No need for collectstatic and STATIC_ROOT
WHITENOISE_USE_FINDERS = True

# Django sets a maximum of 1000 fields per form by default, but particularly complex
# page models can exceed this limit within Wagtail's page editor.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000


# Wagtail settings

WAGTAIL_SITE_NAME = "Universala Kongreso"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = HOST

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]
# WAGTAILEMBEDS_RESPONSIVE_HTML = True

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


# https://docs.djangoproject.com/en/5.2/ref/logging/#default-logging-definition
# Use the console logging in production too
if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {"level": "INFO", "handlers": ["console"]},
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {"handlers": ["console"], "level": "INFO", "propagate": True},
        },
        "formatters": {
            "app": {
                "format": (
                    "%(asctime)s [%(levelname)-8s] "
                    "(%(module)s.%(funcName)s) %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
    }
