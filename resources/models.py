import logging
import os.path
import os
from datetime import datetime

from django.db import models, transaction

from dateutil.tz import tzutc
from reversion import revisions

logger = logging.getLogger(__name__)


class CodeResource(models.Model):
    name = models.CharField(
        max_length=63,
        verbose_name='Nimi',
        help_text='Uniikki tunniste, jolla resurssi ladataan koodista tai HTML:stä käsin.',
        unique=True,
    )

    active = models.BooleanField(
        default=True,
        verbose_name='Aktiivinen',
        help_text='Ei-aktiivisia resursseja ei huomioida.',
    )

    content = models.TextField(
        blank=True,
        verbose_name='Sisältö',
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Muokattu')

    @classmethod
    def ingest(cls, open_file, force=False):
        name = os.path.basename(open_file.name)
        content = open_file.read()

        stat_info = os.stat(open_file.name)
        file_modified = datetime.utcfromtimestamp(stat_info.st_mtime).replace(tzinfo=tzutc())

        with transaction.atomic(), revisions.create_revision():
            revisions.set_comment(f'Ingested {name}')

            try:
                existing = cls.objects.get(name=name)
            except cls.DoesNotExist:
                logger.info('Ingest %s', name)
                return cls.objects.create(name=name, content=content)
            else:
                if file_modified <= existing.updated_at:
                    if force:
                        logger.warn('Ingest %s (force)', name)
                    else:
                        logger.info('Ignore %s (older)', name)
                        return existing
                else:
                    logger.info('Ingest %s (newer)', name)

                existing.content = content
                existing.save()
                return existing

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class StyleSheet(CodeResource):
    class Meta:
        verbose_name = 'Tyylitiedosto'
        verbose_name_plural = 'Tyylitiedostot'


class Template(CodeResource):
    class Meta:
        verbose_name = 'Sivupohja'
        verbose_name_plural = 'Sivupohjat'