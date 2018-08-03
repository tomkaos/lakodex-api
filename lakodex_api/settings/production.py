import dj_database_url
from lakodex_api.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['intense-citadel-86043.herokuapp.com']

CORS_ORIGIN_ALLOW_ALL = True

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config()
}
