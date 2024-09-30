"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=1xydj7(r(tdllcp=7f6b&f$31j7wbj=y*7tez&)5hg@m13qmj"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "SHOES",
    "USER",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
     'allauth.socialaccount.providers.paypal',
    'ORDER',
    'RECOMMENDATION_SYSTEM',  
    
]
SOCIALACCOUNT_PROVIDERS = {
   'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': '286444218104-m0cj32roqe1o2c30f1l8encs1q3lcag8.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
     'paypal': {
        'APP': {
            'client_id': 'AXLrIBrrxt4XL6xsnEI5HJeErkqKBFV4eW16O6x7awAYXmOGPwHVgMU2fs1bW277YqhKtJWtDrBEpGMu',
            'secret': 'EBH0UcqtoD6maODRJ5N5eBB7PtRBE_e0WVxnFGFVZ7vX8nkOJ9OdS9bIWVCGf6U-bWHg9h1yMpFJyjUU',
            'key': ''
        }
    },
}
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # or "live" khi chuyển qua production
    "client_id": "AXLrIBrrxt4XL6xsnEI5HJeErkqKBFV4eW16O6x7awAYXmOGPwHVgMU2fs1bW277YqhKtJWtDrBEpGMu",
    "client_secret": "EBH0UcqtoD6maODRJ5N5eBB7PtRBE_e0WVxnFGFVZ7vX8nkOJ9OdS9bIWVCGf6U-bWHg9h1yMpFJyjUU",
})


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
AUTHENTICATION_BACKENDS = [
   
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shoes_website',
        'USER': 'postgres',
        'PASSWORD': '1021012003',
        'HOST': 'localhost',  
        'PORT': '5432',       
    }
}

# settings.py

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gin21010304@gmail.com'  
EMAIL_HOST_PASSWORD = 'Thanhnhan21010304'  
DEFAULT_FROM_EMAIL = 'ShoeShop@gmail.com'




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR /'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Make email become requirement field
SITE_ID = 1
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_AUTHENTICATION_METHOD ='email'
ACCOUNT_EMAIL_REQUIRED = True






