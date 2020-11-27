from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import (
    Template,
    StyleSheet,
)


RESOURCE_ADMIN_FIELDSETS = (
    (u'Sisältö', dict(
        fields=('name', 'content', 'active'),
    )),
    (u'Lisätiedot', dict(
        fields=('created_at', 'updated_at'),
    )),
)


class StyleSheetAdmin(VersionAdmin):
    list_display = ('name', 'active')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = RESOURCE_ADMIN_FIELDSETS

class TemplateAdmin(VersionAdmin):
    list_display = ('name', 'active')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = RESOURCE_ADMIN_FIELDSETS

admin.site.register(Template, TemplateAdmin)
admin.site.register(StyleSheet, StyleSheetAdmin)