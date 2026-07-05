from django.contrib import admin
from .models import Valorant, ClashOfClan, GamerProfile, HostProfile

# Register your models here.

admin.site.register(Valorant)
admin.site.register(ClashOfClan)
admin.site.register(GamerProfile)
admin.site.register(HostProfile)
