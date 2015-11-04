from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import (
    Template,
    StyleSheet,
)


class StyleSheetAdmin(VersionAdmin):
    pass


class TemplateAdmin(VersionAdmin):
    pass


admin.site.register(Template, TemplateAdmin)
admin.site.register(StyleSheet, StyleSheetAdmin)