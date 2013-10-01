import os
import io

from django.conf import settings
from django.utils.safestring import mark_safe

from django_markup.markup import formatter

from rest_framework.utils.formatting import dedent


# Content Mixins
class FileContentMixin(object):
    def get_content(self, view_cls, html=True, request=None):
        if not request:
            return ""

        if hasattr(self, 'extension'):
            relpath = request.resolver_match.url_name + self.extension
        else:
            relpath = request.resolver_match.url_name

        description_path = os.path.join(
            getattr(settings, 'APIDOC_DOCUMENTATION_PATH', 'apidoc'),
            relpath,
        )
        if not os.path.isfile(description_path):
            return ""

        with io.open(description_path, 'tr') as f:
            return f.read()


class DocStringContentMixin(object):
    def get_content(self, view_cls, html=True, request=None):
        return dedent(view_cls.__doc__ or "")


# Process Mixins
class MarkupProcessMixin(object):
    def process(self, content):
        return mark_safe(formatter(content, filter_name=self.markup))


class NoProcessMixin(object):
    def process(self, content):
        return content


class SafeProcessMixin(object):
    def process(self, content):
        return mark_safe(content)
