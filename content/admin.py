from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Page, BlogPost, Redirect, CommonFields



class PageAdminForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
    )

    class Meta:
        model = Page
        fields = ('site', 'parent', 'slug', 'title', 'body', 'public_from', 'visible_from', 'path')


class PageAdmin(admin.ModelAdmin):
    model = Page
    form = PageAdminForm
    list_display = ('site', 'path', 'title')
    readonly_fields = ('path',)


class BlogPostAdminForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
    )

    class Meta:
        model = BlogPost
        fields = ('site', 'date', 'slug', 'title', 'body', 'public_from', 'visible_from', 'path')


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost
    form = BlogPostAdminForm
    list_display = ('site', 'path', 'title')
    readonly_fields = ('path',)


admin.site.register(Page, PageAdmin)
admin.site.register(Redirect)
admin.site.register(BlogPost, BlogPostAdmin)
