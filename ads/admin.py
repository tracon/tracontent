from django.contrib import admin

from .models import Banner, BannerClick


class BannerAdmin(admin.ModelAdmin):
    model = Banner
    list_display = ('site', 'title', 'url', 'active')
    list_filter = ('site', 'active')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'site':
            kwargs['initial'] = request.site

        return super(BannerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BannerClickAdmin(admin.ModelAdmin):
    model = BannerClick
    list_display = ('site', 'banner', 'date', 'clicks')
    list_filter = ('banner__site',)

    fields = ('banner', 'date', 'clicks')
    readonly_fields = ('banner', 'date', 'clicks')

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerClick, BannerClickAdmin)
