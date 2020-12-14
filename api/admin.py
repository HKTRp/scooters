from django.contrib import admin

from .models import *

admin.site.register(Scooter)
admin.site.register(Order)
admin.site.register(Client)
admin.site.register(Transaction)
admin.site.register(Rate)
admin.site.register(ClientsGroup)
admin.site.register(ScootersGroup)
admin.site.register(RateGroup)
admin.site.register(Alert)
admin.site.register(GeoPoint)
admin.site.register(GeoZone)
admin.site.register(AlarmSettingsSingleton)
