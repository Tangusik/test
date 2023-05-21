from django.contrib import admin
from .models import Client, Address, Team, Trainer, Activity

admin.site.register(Activity)
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(Team)
admin.site.register(Trainer)