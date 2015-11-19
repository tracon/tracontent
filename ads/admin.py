from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Banner, BannerClick


class BannerAdmin(VersionAdmin):
    model = Banner
    list_display = ('admin_get_sites', 'title', 'url', 'active')
    list_filter = ('sites', 'active')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'sites':
            kwargs['initial'] = [request.site]

        return super(BannerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BannerClickAdmin(admin.ModelAdmin):
    model = BannerClick
    list_display = ('site', 'banner', 'date', 'clicks')
    list_filter = ('site',)

    fields = ('banner', 'date', 'clicks')
    readonly_fields = ('banner', 'date', 'clicks')

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerClick, BannerClickAdmin)
