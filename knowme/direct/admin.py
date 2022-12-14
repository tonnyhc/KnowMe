from django.contrib import admin

from knowme.direct.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
