# encoding: utf-8

import logging
import os.path
import os
from datetime import datetime

from django.db import models, transaction

from dateutil.tz import tzutc
import reversion

logger = logging.getLogger(__name__)


class CodeResource(models.Model):
    name = models.CharField(
        max_length=63,
        verbose_name=u'Nimi',
        help_text=u'Uniikki tunniste, jolla resurssi ladataan koodista tai HTML:stä käsin.',
        unique=True,
    )

    active = models.BooleanField(
        default=True,
        verbose_name=u'Aktiivinen',
        help_text=u'Ei-aktiivisia resursseja ei huomioida.',
    )

    content = models.TextField(
        blank=True,
        verbose_name=u'Sisältö',
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Muokattu')

    @classmethod
    def ingest(cls, open_file, force=False):
        name = os.path.basename(open_file.name)
        content = open_file.read()

        stat_info = os.stat(open_file.name)
        file_modified = datetime.utcfromtimestamp(stat_info.st_mtime).replace(tzinfo=tzutc())

        with transaction.atomic(), reversion.create_revision():
            reversion.set_comment('Ingested {name}'.format(name=name))

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

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class StyleSheet(CodeResource):
    class Meta:
        verbose_name = u'Tyylitiedosto'
        verbose_name_plural = u'Tyylitiedostot'


class Template(CodeResource):
    class Meta:
        verbose_name = u'Sivupohja'
        verbose_name_plural = u'Sivupohjat'