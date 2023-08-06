# Fyle Rest Auth

Django application to implement OAuth 2.0 using Fyle in Django rest framework


## Installation

This project requires [Python 3+](https://www.python.org/downloads/) and [Requests](https://pypi.org/project/requests/) library (pip install requests).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).
        
        $ pip install fyle-rest-auth

## Usage

To use this Django app you'll need fyle credentials used for OAuth2 authentication: **client ID**, **client secret** and **refresh token**.

* Add fyle rest auth in INSTALLED_APPS in settings file
```pythonstub
INSTALLED_APPS = [
    ...,
    'fyle_rest_auth'
]
```

* Add authentication class to settings file
```pythonstub
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'fyle_rest_auth.authentication.FyleJWTAuthentication',
    ),
}
```

* Add serializer path in settings file
```pythonstub
FYLE_REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer'
}
```

* Add the constants in settings file
```pythonstub
FYLE_BASE_URL = '<Fyle Base URL>'
FYLE_TOKEN_URI = '<Fyle Token URI>'
FYLE_CLIENT_ID = '<Fyle Client Id>'
FYLE_CLIENT_SECRET = '<Fyle Client Secret>'
```

* Include urls in the the django app.
```pythonstub
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('fyle_rest_auth.urls')),
    
]
```
* Configure cache in settings file
```pythonstub
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'your_cache_table',
    }
}
```

* Creating the cache table
```pythonstub
python manage.py createcachetable
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
