from django.contrib import admin
from .models import Messages,AfterRegistration,EveryDay,SpecificDay,Events

@admin.register(Messages)
@admin.register(AfterRegistration)
@admin.register(EveryDay)
@admin.register(SpecificDay)
@admin.register(Events)
class AuthorAdmin(admin.ModelAdmin):
    pass