from django.db import models

DAY_CHOICES = [
    ("vkl", "Koko viikonloppu"),
    ("la", "Vain lauantai"),
    ("su", "Vain sunnuntai"),
]


class Day(models.Model):
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE)
    order_number = models.PositiveSmallIntegerField()
    slug = models.CharField(max_length=63)
    name = models.CharField(max_length=63)

    class Meta:
        unique_together = [("site", "slug")]
        ordering = ("site", "order_number")

    def __str__(self):
        return self.name


class Artist(models.Model):
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE)
    days = models.ManyToManyField(Day, blank=True)
    table_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    homepage_url = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    image_file = models.ImageField(upload_to="artists", blank=True)

    def __str__(self):
        return self.name

    @property
    def formatted_days(self):
        return ", ".join(day.name for day in self.days.all()).capitalize()

    def admin_days(self):
        return self.formatted_days

    admin_days.short_description = "Päivät"
    admin_days.admin_order_field = "days"

    class Meta:
        verbose_name = "taiteilija"
        verbose_name_plural = "taiteilijat"
        ordering = ("site", "table_number", "name")
