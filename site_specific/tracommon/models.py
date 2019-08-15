from django.db import models


DAY_CHOICES = [
    ('vkl', 'Koko viikonloppu'),
    ('la', 'Vain lauantai'),
    ('su', 'Vain sunnuntai'),
]


class Artist(models.Model):
    site = models.ForeignKey('sites.Site')
    day = models.CharField(max_length=max(len(i) for (i, j) in DAY_CHOICES), default=DAY_CHOICES[0][0], choices=DAY_CHOICES)
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
