from django.contrib import admin

from .models import Organizer


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'nick', 'job_title', 'email')


admin.site.register(Organizer, OrganizerAdmin)