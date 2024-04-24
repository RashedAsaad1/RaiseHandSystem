from django.contrib import admin  # Importerar admin-modulen från Django.

from .models import (group,Login)  # Importerar modellerna 'group' och 'Login' från den aktuella modulens 'models'-modul.

admin.site.register(group)  # Registrerar modellen 'group' så att den kan hanteras i Django-administrationsgränssnittet.
admin.site.register(Login)  # Registrerar modellen 'Login' så att den kan hanteras i Django-administrationsgränssnittet.