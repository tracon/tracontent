from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Artist


class ArtistAdmin(VersionAdmin):
    model = Artist
    list_display = ('site', 'day', 'table_number', 'name')
    list_filter = ('site', 'day')
    search_fields = ('table_number', 'name')


admin.site.register(Artist, ArtistAdmin)
