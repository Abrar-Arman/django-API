import os

from dotenv import load_dotenv

load_dotenv()
env = os.environ.get("DJANGO_ENV")

if env == "production":
    from .production import *
else:
    from .development import *
