# encoding: utf-8

import re


SLUGIFY_CHAR_MAP = {
  u'ä': u'a',
  u'å': u'a',
  u'ö': u'o',
  u'ü': u'u',
  u' ': u'-',
  u'_': u'-',
  u'.': u'-',
}
SLUGIFY_FORBANNAD_RE = re.compile(ur'[^a-z0-9-]', re.UNICODE)
SLUGIFY_MULTIDASH_RE = re.compile(ur'-+', re.UNICODE)


def slugify(ustr):
    ustr = ustr.lower()
    ustr = u''.join(SLUGIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = SLUGIFY_FORBANNAD_RE.sub(u'', ustr)
    ustr = SLUGIFY_MULTIDASH_RE.sub(u'-', ustr)
    return ustr
