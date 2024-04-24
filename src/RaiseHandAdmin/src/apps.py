from django.apps import AppConfig 

class RaiseConfig(AppConfig):
    """A Django application configuration class for the 'src' application.

    This class inherits from Django's AppConfig class and sets the default
    auto field type and the name of the application.

    Attributes:
        default_auto_field (str): Defines the type of auto-created primary key. Defaults to 'django.db.models.BigAutoField'.
        name (str): Defines the name of the application. Defaults to 'src'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'