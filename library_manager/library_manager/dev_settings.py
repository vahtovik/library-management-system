from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*)6@)=qtxpofgtdghnms@saps=[;zx414312c]awsasdasdg32bxen%710g8*$h123jlrewz'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
