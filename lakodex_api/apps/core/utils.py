import hashlib
import importlib
import string
from collections import OrderedDict
from django.utils import six
from django.utils.six.moves.urllib.parse import urlsplit


def create_avatar_url(email, size=100, default='identicon', rating='g'):
    url = 'http://www.gravatar.com/avatar'

    hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)


def import_attribute(path):
    assert isinstance(path, six.string_types)
    pkg, attr = path.rsplit('.', 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret
