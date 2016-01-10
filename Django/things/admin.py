from django.contrib import admin

# Register your models here.
from .models import Thing, Value, Controller, Sensor, AutomaticController

admin.site.register(Thing)
admin.site.register(Value)
admin.site.register(Controller)
admin.site.register(Sensor)
admin.site.register(AutomaticController)