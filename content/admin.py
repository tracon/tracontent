# encoding: utf-8

from django.contrib import admin
from django.contrib.sites.models import Site
from django.forms import ValidationError
from django.utils.timezone import now
from django import forms

from ckeditor.widgets import CKEditorWidget
from reversion.admin import VersionAdmin

from .models import (
    BlogCategory,
    BlogComment,
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


def make_is_null_list_filter(field_name, title, yes_is_null=False):
    _title = title
    _parameter_name = "{field_name}__isnull".format(field_name=field_name)

    class _IsNullListFilter(admin.SimpleListFilter):
        title = _title
        parameter_name = _parameter_name

        def lookups(self, request, model_admin):
            return (
                (1, u'Kyllä'),
                (0, u'Ei'),
            )

        def queryset(self, request, queryset):
            if self.value() is not None:
                if yes_is_null:
                    return queryset.filter(**{_parameter_name: bool(int(self.value()))})
                else:
                    return queryset.filter(**{_parameter_name: not bool(int(self.value()))})


    return _IsNullListFilter



def make_selected_pages_private(modeladmin, request, queryset):
    queryset.update(public_from=None, visible_from=None)
make_selected_pages_private.short_description = u'Aseta valittujen sivujen tila: ei julkinen, ei näkyvissä'


def make_selected_pages_public(modeladmin, request, queryset):
    t = now()
    queryset.update(public_from=t, visible_from=None)
make_selected_pages_public.short_description = u'Aseta valittujen sivujen tila: julkinen, ei näkyvissä'


def make_selected_pages_visible(modeladmin, request, queryset):
    t = now()
    queryset.update(public_from=t, visible_from=t)
make_selected_pages_visible.short_description = u'Aseta valittujen sivujen tila: julkinen, näkyvissä'


ActiveListFilter = make_is_null_list_filter('removed_at', u'Näkyvissä', yes_is_null=True)
PublishedListFilter = make_is_null_list_filter('public_from', u'Julkinen')
VisibleListFilter = make_is_null_list_filter('visible_from', u'Näkyvissä')


class PageAdminForm(forms.ModelForm, CommonAdminFormMixin):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
        required=not CommonFields.body['blank'],
    )

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)

        if self.instance:
            try:
                self.fields['parent'].queryset = self.instance.site.page_set.all()
            except Site.DoesNotExist:
                pass

    def clean_site(self):
        site = self.cleaned_data.get('site')
        parent = self.cleaned_data.get('parent')

        if site and parent and parent.site != site:
            raise forms.ValidationError(u'Yläsivun tulee olla valitulla sivustolla')

        return site

    class Meta:
        model = Page
        fields = ('site', 'parent', 'slug', 'title', 'body', 'public_from', 'visible_from', 'path', 'order', 'override_menu_text')


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


class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)


class PageAdmin(VersionAdmin):
    model = Page
    form = PageAdminForm
    list_display = ('site', 'path', 'title', 'admin_is_published', 'admin_is_visible')
    list_filter = ('site', PublishedListFilter, VisibleListFilter)
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
            fields=('site', 'order', 'slug', 'path', 'override_menu_text', 'created_at', 'updated_at'),
            classes=('collapse',),
        ))
    )

    @classproperty
    def actions(cls):
        _actions = [make_selected_pages_private, make_selected_pages_public, make_selected_pages_visible]

        for site in Site.objects.all():
            def _copy_to_site(modeladmin, request, queryset, _site=site):
                for page in queryset.all():
                    page.copy_to_site(_site)
            _copy_to_site.__name__ = "copy_to_site_{id}".format(id=site.id)
            _copy_to_site.short_description = "Kopioi valitut sivut luonnoksiksi sivustoon: {domain}".format(domain=site.domain)

            _actions.append(_copy_to_site)

        return _actions

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'site':
            kwargs['initial'] = request.site

        return super(PageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RedirectAdmin(VersionAdmin):
    model = Redirect
    list_display = ('site', 'path', 'target')
    list_filter = ('site',)


class BlogPostAdminForm(forms.ModelForm, CommonAdminFormMixin):
    body = forms.CharField(
        widget=CKEditorWidget(),
        label=CommonFields.body['verbose_name'],
        required=not CommonFields.body['blank'],
    )

    def __init__(self, *args, **kwargs):
        super(BlogPostAdminForm, self).__init__(*args, **kwargs)

        self.fields['date'].initial = now().date()

        try:
            site = self.instance.site
        except Site.DoesNotExist:
            pass
        else:
            if site:
                self.fields['categories'].queryset = BlogCategory.objects.filter(site=site)

    def clean(self):
        cleaned_data = super(BlogPostAdminForm, self).clean()
        site = self.cleaned_data.get('site')
        categories = self.cleaned_data.get('categories')

        if categories and site and any(category.site != site for category in categories):
            raise ValidationError(u'Kaikkien kategorioiden, joihin postaus kuuluu, tulee olla samalla sivustolla postauksen kanssa.')

    class Meta:
        model = BlogPost
        fields = ('site', 'date', 'slug', 'title', 'override_excerpt', 'body', 'public_from', 'visible_from', 'path', 'author')


class BlogPostAdmin(VersionAdmin):
    model = BlogPost
    form = BlogPostAdminForm
    list_display = ('site', 'path', 'title', 'state', 'admin_is_published', 'admin_is_visible')
    list_filter = ('site', 'state', PublishedListFilter, VisibleListFilter)
    readonly_fields = ('path', 'created_at', 'updated_at')
    view_on_site = True
    fieldsets = (
        (u'Sisältö', dict(
            fields=('title', 'override_excerpt', 'body'),
        )),
        (u'Sisäiset muistiinpanot', dict(
            fields=('state', 'internal_notes'),
        )),
        (u'Julkaisuasetukset', dict(
            fields=('date', 'public_from', 'visible_from', 'categories', 'is_featured'),
        )),
        (u'Lisäasetukset', dict(
            fields=('site', 'slug', 'author', 'path', 'created_at', 'updated_at'),
            classes=('collapse',),
        ))
    )
    actions = [make_selected_pages_private, make_selected_pages_public, make_selected_pages_visible]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'site':
            kwargs['initial'] = request.site
        elif db_field.name == 'author':
            kwargs['initial'] = request.user

        return super(BlogPostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


def hide_selected_blog_comments(modeladmin, request, queryset):
    t = now()
    queryset.update(removed_at=t, removed_by=request.user)
hide_selected_blog_comments.short_description = u'Piilota valitut blogikommentit'

def restore_selected_blog_comments(modeladmin, request, queryset):
    queryset.update(removed_at=None, removed_by=None)
restore_selected_blog_comments.short_description = u'Palauta valitut blogikommentit'


class BlogCommentAdminForm(forms.ModelForm):
    is_active = forms.BooleanField(label=u'Näkyvissä', help_text=u'Poistamalla ruksin tästä voit piilottaa asiattoman kommentin sivustolta.', required=False)

    def __init__(self, *args, **kwargs):
        super(BlogCommentAdminForm, self).__init__(*args, **kwargs)

        self.fields['is_active'].initial = self.instance.removed_at is None

    class Meta:
        model = BlogComment
        fields = ()


class BlogCommentAdmin(admin.ModelAdmin):
    model = BlogComment
    form = BlogCommentAdminForm
    list_display = ('admin_get_site', 'blog_post', 'created_at', 'admin_get_excerpt', 'author_name', 'admin_is_active')
    list_filter = ('blog_post__site', ActiveListFilter)
    readonly_fields = ('blog_post', 'created_at', 'author_name', 'author_email', 'author_ip_address', 'comment', 'removed_at', 'removed_by')
    actions = [hide_selected_blog_comments, restore_selected_blog_comments]

    fieldsets = (
        (u'Kommentti', dict(
            fields=('blog_post', 'created_at', 'comment'),
        )),
        (u'Kirjoittaja', dict(
            fields=('author_name', 'author_email', 'author_ip_address'),
        )),
        (u'Moderointi', dict(
            fields=('is_active', 'removed_at', 'removed_by'),
        ))
    )

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def get_actions(self, request):
        actions = super(BlogCommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        blog_comment = obj
        is_active = form.cleaned_data['is_active']

        if is_active and not blog_comment.is_active:
            blog_comment.removed_at = None
            blog_comment.removed_by = None
            blog_comment.save()
        elif not is_active and blog_comment.is_active:
            blog_comment.removed_at = now()
            blog_comment.removed_by = request.user
            blog_comment.save()


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('site', 'slug', 'title')
    list_filter = ('site',)
    search_fields = ('slug', 'title')


admin.site.register(Page, PageAdmin)
admin.site.register(Redirect, RedirectAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(SiteSettings)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
