from django.contrib import admin

from .models import Page, BlogPost, Redirect


class PageAdmin(admin.ModelAdmin):
    model = Page
    list_display = ('site', 'path', 'title')
    fields = ('site', 'parent', 'slug', 'title', 'body', 'public_from', 'visible_from', 'path')
    readonly_fields = ('path',)


admin.site.register(Page, PageAdmin)
admin.site.register(Redirect)
admin.site.register(BlogPost)
