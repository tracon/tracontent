import logging

from django.template.loaders.base import Loader
from django.template.loader import LoaderOrigin
from django.template import TemplateDoesNotExist

from .models import Template


logger = logging.getLogger(__name__)


class DatabaseTemplateLoader(Loader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            template = Template.objects.get(name=template_name, active=True)
        except Template.DoesNotExist:
            logger.debug('Template %s not found in database', template_name)
            raise TemplateDoesNotExist(template_name)
        else:
            logger.debug('Template %s found in database', template_name)
            return template.content, template_name