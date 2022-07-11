from django.contrib import admin
from django.forms import ModelForm, ValidationError

from reversion.admin import VersionAdmin

from .models import Artist, Day


class ArtistAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            site = self.instance.site
        else:
            site = self.fields["site"].initial

        self.fields["days"].queryset = Day.objects.filter(site=site)

    def clean(self):
        cleaned_data = super().clean()
        site = self.cleaned_data.get("site")
        days = self.cleaned_data.get("days")

        if days and site and any(category.site != site for category in days):
            raise ValidationError(
                "Kaikkien päivien, joihin taiteilija kuuluu, "
                "tulee olla samalla sivustolla taiteilijan kanssa."
            )

    class Meta:
        model = Artist
        fields = (
            "site",
            "days",
            "table_number",
            "name",
            "homepage_url",
            "description",
            "image_file",
        )


class ArtistAdmin(VersionAdmin):
    model = Artist
    form = ArtistAdminForm
    list_display = ("site", "admin_days", "table_number", "name")
    list_filter = ("site", "days")
    search_fields = ("table_number", "name")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "site":
            kwargs["initial"] = request.site

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Artist, ArtistAdmin)
