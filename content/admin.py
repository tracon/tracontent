# encoding: utf-8

from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Page, BlogPost, Redirect, CommonFields


class CommonAdminFormMixin(object):
    def clean_visible_from(self):
        public_from = self.cleaned_data.get('public_from')
        visible_from = self.cleaned_data.get('visible_from')

        if visible_from:
            if not public_from:
                raise forms.ValidationError(u'Jotta sivu voi olla näkyvissä, sen tulee myös olla julkinen')
            elif public_from > visible_from:
                raise forms.ValidationError(u'Sivun täytyy tulla julkiseksi viimeistään samalla hetkellä kun se tulee näkyväksi')

        return visible_from


class PageAdminForm(CommonAdminFormMixin, forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
        required=not CommonFields.body['blank'],
    )

    def clean_parent(self):
        site = self.cleaned_data.get('site')
        parent = self.cleaned_data.get('parent')

        if site and parent and parent.site != site:
            raise forms.ValidationError(u'Yläsivun tulee olla valitulla sivustolla')

        return parent

    class Meta:
        model = Page
        fields = ('site', 'parent', 'slug', 'title', 'body', 'public_from', 'visible_from', 'path', 'order')


class PageAdminTabularInline(admin.TabularInline):
    model = Page
    extra = 0
    fields = ('order', 'slug', 'title')
    readonly_fields = ('slug', 'title')
    can_delete = False
    show_change_link = True
    verbose_name = u'alasivujen järjestys'
    verbose_name_plural = u'alasivujen järjestys'
    max_num = 0


class PageAdmin(admin.ModelAdmin):
    model = Page
    form = PageAdminForm
    list_display = ('site', 'path', 'title')
    list_filter = ('site',)
    readonly_fields = ('path',)
    view_on_site = True
    ordering = ('site', 'parent', 'order')
    search_fields = ('path', 'title')
    inlines = (PageAdminTabularInline,)
    fieldsets = (
        (u'Sivun sijainti', dict(
            fields=('site', 'parent')
        )),
        (u'Sisältö', dict(
            fields=('title', 'body')
        )),
        (u'Julkaisuasetukset', dict(
            fields=('public_from', 'visible_from')
        )),
        (u'Tekniset tiedot', dict(
            fields=('slug', 'order'),
            classes=('collapse',),
        ))
    )


class BlogPostAdminForm(CommonAdminFormMixin, forms.ModelForm):
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
