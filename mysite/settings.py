"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9l$ef-y(q$3ixo*oziug4)z8y6#$vz9)#vh@ne^%-%wnd8z56i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SEND = False

ALLOWED_HOSTS = ['167.172.128.142','127.0.0.1', 'www.circledin.io']

#ALLOWED_HOSTS = []

SITE_REDIRECT_ORIGINAL = "https://www.circledin.io"
# SITE_REDIRECT_ORIGINAL = "http://127.0.0.1:8000"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps',
    'django.contrib.humanize',
    'bootstrap_datepicker_plus',
    'django_social_share',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'apps/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# DATABASES = {
#     'default': {
#      'ENGINE': 'django.db.backends.mysql',
#       'NAME': 'CircledIn_Db',
#        'USER': 'root',
#         'PASSWORD':'i;)LM;v$kFwHx$0T3X64G<.cKXgf)!Eu',
#         'HOST':'ls-ae48dd21c525115c6693356db343ed93aeb0cdb9.cn5zbpbn48n2.us-east-1.rds.amazonaws.com',
#         'PORT':'3306'

#   }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'



#--------------------------------------------------------------------------
from django.urls import reverse_lazy

LOGIN_REDIRECT_URL = reverse_lazy('dashboard')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
#--------------------------------------------------------------------------


#------------------------------------------------------------------------
#Email Setting...
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'futuresoftcode@gmail.com'
EMAIL_HOST_PASSWORD = 'Sul03314307703'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# SENDGRID_API_KEY = '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'

#-------------------------------------------------------------------------


#------------------------------------------------------------------------
#Media settings
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'
SSTATICFILES_DIRS=[
    STATIC_ROOT,

    ]
MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
#MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(os.path.dirname(BASE_DIR),'media')
#-------------------------------------------------------------------------


#--------------------------------------------------------------------
#Authentication Backends...

AUTHENTICATION_BACKENDS=[
    'apps.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    
]
#--------------------------------------------------------------------

#####################################################################
STRIPE_SECRET_KEY = 'sk_test_jAndihGEFE8VtiRfUfTyygxH00JNgys3DY'
STRIPE_PUBLISHABLE_KEY = 'pk_test_7Caol5AeV11tgvLYCf7FlGXr00hMYbhIfm'
STRIPE_PLAN_MONTHLY_ID = 'plan_HFv9CmBmgpSKED'
#####################################################################


BOOTSTRAP4 = {
    'include_jquery': True,
}



# For session expire
SESSION_COOKIE_AGE = 30*60  #  define number of seconds
