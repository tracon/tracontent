# encoding: utf-8

from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Page, BlogPost, Redirect, CommonFields


class PageAdminForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
        required=not CommonFields.body['blank'],
    )

    def clean_visible_from(self):
        public_from = self.cleaned_data.get('public_from')
        visible_from = self.cleaned_data.get('visible_from')

        if visible_from:
            if not public_from:
                raise forms.ValidationError(u'Jotta sivu voi olla näkyvissä, sen tulee myös olla julkinen')
            elif public_from > visible_from:
                raise forms.ValidationError(u'Sivun täytyy tulla julkiseksi viimeistään samalla hetkellä kun se tulee näkyväksi')

        return visible_from

    class Meta:
        model = Page
        fields = ('site', 'parent', 'slug', 'title', 'body', 'public_from', 'visible_from', 'path')


class PageAdmin(admin.ModelAdmin):
    model = Page
    form = PageAdminForm
    list_display = ('site', 'path', 'title')
    list_filter = ('site',)
    readonly_fields = ('path',)
    view_on_site = True


class BlogPostAdminForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
        required=not CommonFields.body['blank'],
    )

    class Meta:
        model = BlogPost
        fields = ('site', 'date', 'slug', 'title', 'body', 'public_from', 'visible_from', 'path')


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost
    form = BlogPostAdminForm
    list_display = ('site', 'path', 'title')
    list_filter = ('site',)
    readonly_fields = ('path',)
    view_on_site = True


admin.site.register(Page, PageAdmin)
admin.site.register(Redirect)
admin.site.register(BlogPost, BlogPostAdmin)
