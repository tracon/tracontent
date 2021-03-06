import re

import loremipsum
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden


SLUGIFY_CHAR_MAP = {
  'ä': 'a',
  'å': 'a',
  'ö': 'o',
  'ü': 'u',
  ' ': '-',
  '_': '-',
  '.': '-',
}
SLUGIFY_FORBANNAD_RE = re.compile(r'[^a-z0-9-]', re.UNICODE)
SLUGIFY_MULTIDASH_RE = re.compile(r'-+', re.UNICODE)


def slugify(ustr):
    ustr = ustr.lower()
    ustr = ''.join(SLUGIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = SLUGIFY_FORBANNAD_RE.sub('', ustr)
    ustr = SLUGIFY_MULTIDASH_RE.sub('-', ustr)
    return ustr


def make_horizontal_form_helper(helper):
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-9'
    return helper


def horizontal_form_helper():
    return make_horizontal_form_helper(FormHelper())


def indented_without_label(input, css_class='col-md-offset-3 col-md-9'):
    return Div(Div(input, css_class=f'controls {css_class}'), css_class='form-group')


def initialize_form(FormClass, request, **kwargs):
    if request.method == 'POST':
        form = FormClass(request.POST, **kwargs)
    else:
        form = FormClass(**kwargs)

    return form


def pick_attrs(obj, *attr_names, **extra_attrs):
    return dict(
      ((attr_name, getattr(obj, attr_name)) for attr_name in attr_names),
      **extra_attrs
    )


def format_emails(names_and_addresses):
    return [
      f"{name} <{address}>"
      for (name, address) in names_and_addresses
    ]


def get_code(path):
    """
    Given "core.utils:get_code", imports the module "core.utils" and returns
    "get_code" from it.
    """
    from importlib import import_module
    module_name, member_name = path.split(':')
    module = import_module(module_name)
    return getattr(module, member_name)


def lorem(paragraphs=5):
    return '\n\n'.join(
        '<p>{}</p>'.format(par)
        for par in loremipsum.get_paragraphs(paragraphs, start_with_lorem=True)
    )


def groups_of_n(iterable, n):
    groups = []
    cur_group = []
    for item in iterable:
        cur_group.append(item)
        if len(cur_group) == n:
            groups.append(cur_group)
            cur_group = []

    if cur_group:
        groups.append(cur_group)

    return groups