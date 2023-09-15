from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_APPS = [
    "apps.user",
    "apps.post",
    "apps.core",
]

THIRD_PARTY_APPS = []

INSTALLED_APPS = [*DEFAULT_APPS, *CUSTOM_APPS, *THIRD_PARTY_APPS]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.log.LogRequestAndResponseMiddleware",
    "apps.core.middleware.filter.BlockBrowserByUA",
    "apps.core.middleware.view_perf.LogViewExecutionTimeMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"
STATICFILES_DIRS = [
    str(BASE_DIR / "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# needed to use the user model from the user app
AUTH_USER_MODEL = 'user.User'

# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = BASE_DIR / "media"

# Encrypt Cookies on the client
SESSION_COOKIE_SECURE = True

# Redirect the user to this url if user is not authenticated
LOGIN_URL = "home"

# Logger configuration
LOGGING = {
    "version": 1, # dictConfig format version
    "loggers": {
        "logging_mw": { # specify the logger instance
            "handlers": ["file_req_res", "console"],
            "level": "DEBUG", 
        },
        "view_performance": {
            "handlers": ["file_perf", "console"],
            "level": "DEBUG",
        },
    },
    "handlers": {
            "console": {
                "level": "WARNING", 
                "class": "logging.StreamHandler", 
                "formatter": "verbose",
                "filters": ["dev_only",], # only print to console when DEBUG=True
            },
            "file_req_res": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": str(BASE_DIR / "logs" / "req_res_logs.log"),
                "formatter": "verbose",
            },
            "file_perf": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": str(BASE_DIR / "logs" / "view_runtime_logs.log"),
                "formatter": "perf",
            },
    },
    "formatters": {
        "verbose": { 
            "format": "[{levelname}] {asctime} :: {module} :: {message}",
            "style": "{", # define the style used in 'format'
        },
        "perf": { 
            "format": "[{levelname}] {asctime} :: {message}",
            "style": "{",
        },
    },
    "filters": {
        "dev_only": { 
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
}