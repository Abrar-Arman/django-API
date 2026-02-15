import os

from dotenv import load_dotenv

from .base import *

DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
load_dotenv()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": "db",
        "PORT": "5432",
        "CONN_MAX_AGE": 0,
    }
}
