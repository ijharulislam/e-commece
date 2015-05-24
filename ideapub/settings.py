"""
Django settings for ideapub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def path(*x):
    """Get and return the relative path of x."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)




AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kf4nn&5tq9=*&qu1urmt)tbk4k!ed_cw*gfys&^@luf#1g6y+h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party 
    #'taggit',
    'ckeditor',
    'django.contrib.sites',
    'sorl.thumbnail',
    'pipeline',


    # Ideapub Apps
    'accounts',
    'pages',
    'sales',
    'financial',
    'catalog',
    'geo',
    'payments',
    'config',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    
    # Required by allauth template tags
    "django.core.context_processors.request",
    # allauth specific context processors
    'django.contrib.auth.context_processors.auth',

)




ROOT_URLCONF = 'ideapub.urls'

WSGI_APPLICATION = 'ideapub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/



STATIC_URL = '/static/'

CKEDITOR_UPLOAD_PATH = 'media/'

STATIC_ROOT = 'static'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 1000,
    },
}
CKEDITOR_IMAGE_BACKEND = 'pillow'

MEDIA_ROOT = os.path.join(os.path.dirname (__file__), 'media')
MEDIA_URL = '/media/'

FEEDBACK_ADMIN_EMAIL = 'ijharalkawsary@gmail.com'




PAGE_VIEWS = (('pages_base_page', 'Base View'),
              ('pages_catalog_page', 'Catalog View')
)