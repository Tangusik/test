from django.contrib import admin
from .models import Client, Address, Team, Trainer, Activity, Sport, News, ClientStatus, TrainerStatus

admin.site.register(Activity)
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(Team)
admin.site.register(Trainer)
admin.site.register(Sport)
admin.site.register(ClientStatus)
admin.site.register(TrainerStatus)
admin.site.register(News)