from django.db import models


class Artist(models.Model):
    site = models.ForeignKey('sites.Site')
    table_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    homepage_url = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    image_file = models.ImageField(upload_to='artists', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'taiteilija'
        verbose_name_plural = 'taiteilijat'
        ordering = ('site', 'table_number', 'name')
