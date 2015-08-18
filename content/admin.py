# encoding: utf-8

from django.contrib import admin
from django.utils.timezone import now
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import (
    BlogPost,
    BlogComment,
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
    readonly_fields = ('path', 'created_at', 'updated_at')
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
            fields=('site', 'order', 'slug', 'path', 'created_at', 'updated_at'),
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
    readonly_fields = ('path', 'created_at', 'updated_at')
    view_on_site = True
    fieldsets = (
        (u'Sisältö', dict(
            fields=('title', 'override_excerpt', 'body'),
        )),
        (u'Julkaisuasetukset', dict(
            fields=('date', 'public_from', 'visible_from'),
        )),
        (u'Lisäasetukset', dict(
            fields=('site', 'slug', 'author', 'path', 'created_at', 'updated_at'),
            classes=('collapse',),
        ))
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'site':
            kwargs['initial'] = request.site
        elif db_field.name == 'author':
            kwargs['initial'] = request.user

        return super(BlogPostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



class ActiveListFilter(admin.SimpleListFilter):
    title = u'Näkyvissä'
    parameter_name = 'removed_at__isnull'

    def lookups(self, request, model_admin):
        return (
            (1, u'Kyllä'),
            (0, u'Ei'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(removed_at__isnull=bool(int(self.value())))


def hide_selected_blog_posts(modeladmin, request, queryset):
    t = now()
    queryset.update(removed_at=t, removed_by=request.user)
hide_selected_blog_posts.short_description = u'Piilota valitut blogikommentit'

def restore_selected_blog_posts(modeladmin, request, queryset):
    queryset.update(removed_at=None, removed_by=None)
restore_selected_blog_posts.short_description = u'Palauta valitut blogikommentit'


class BlogCommentAdmin(admin.ModelAdmin):
    model = BlogComment
    list_display = ('admin_get_site', 'blog_post', 'created_at', 'admin_get_excerpt', 'author_name', 'admin_is_active')
    list_filter = ('blog_post__site', ActiveListFilter)
    fields = ('blog_post', 'author_name', 'author_email', 'author_ip_address', 'comment', 'removed_at', 'removed_by')
    readonly_fields = fields
    actions = [hide_selected_blog_posts, restore_selected_blog_posts]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def get_actions(self, request):
        actions = super(BlogCommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(Page, PageAdmin)
admin.site.register(Redirect)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(SiteSettings)
admin.site.register(BlogComment, BlogCommentAdmin)
