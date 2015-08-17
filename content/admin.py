# encoding: utf-8

from django.contrib import admin
from django.utils.timezone import now
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import (
    BlogPost,
    CommonFields,
    Page,
    Redirect,
    SiteSettings,
)


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


class PageAdminForm(forms.ModelForm, CommonAdminFormMixin):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
        required=not CommonFields.body['blank'],
    )

    def clean_site(self):
        site = self.cleaned_data.get('site')
        parent = self.cleaned_data.get('parent')

        if site and parent and parent.site != site:
            raise forms.ValidationError(u'Yläsivun tulee olla valitulla sivustolla')

        return site

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
        (u'Sisältö', dict(
            fields=('title', 'body')
        )),
        (u'Julkaisuasetukset', dict(
            fields=('parent', 'public_from', 'visible_from')
        )),
        (u'Lisäasetukset', dict(
            fields=('site', 'slug', 'order', 'path'),
            classes=('collapse',),
        ))
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'site':
            kwargs['initial'] = request.site

        return super(PageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BlogPostAdminForm(forms.ModelForm, CommonAdminFormMixin):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
        required=not CommonFields.body['blank'],
    )

    def __init__(self, *args, **kwargs):
        super(BlogPostAdminForm, self).__init__(*args, **kwargs)

        self.fields['date'].initial = now().date()

    class Meta:
        model = BlogPost
        fields = ('site', 'date', 'slug', 'title', 'override_excerpt', 'body', 'public_from', 'visible_from', 'path', 'author')


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost
    form = BlogPostAdminForm
    list_display = ('site', 'path', 'title')
    list_filter = ('site',)
    readonly_fields = ('path',)
    view_on_site = True
    fieldsets = (
        (u'Sisältö', dict(
            fields=('title', 'override_excerpt', 'body'),
        )),
        (u'Julkaisuasetukset', dict(
            fields=('date', 'public_from', 'visible_from'),
        )),
        (u'Lisäasetukset', dict(
            fields=('site', 'slug', 'author', 'path'),
            classes=('collapse',),
        ))
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'site':
            kwargs['initial'] = request.site
        elif db_field.name == 'author':
            kwargs['initial'] = request.user

        return super(BlogPostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Page, PageAdmin)
admin.site.register(Redirect)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(SiteSettings)
