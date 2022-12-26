from django.contrib import admin
from chat_app.models import *

# Register your models here.

@admin.register(Chat)
class Chatadmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Chat._meta.fields
        ]


@admin.register(Group)
class Groupadmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Group._meta.fields
        ]