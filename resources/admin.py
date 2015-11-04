from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import (
    Template,
    StyleSheet,
)


class StyleSheetAdmin(VersionAdmin):
    list_display = ('name', 'active')


class TemplateAdmin(VersionAdmin):
    list_display = ('name', 'active')


admin.site.register(Template, TemplateAdmin)
admin.site.register(StyleSheet, StyleSheetAdmin)