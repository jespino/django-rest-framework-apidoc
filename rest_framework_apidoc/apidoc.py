from django.conf import settings

from rest_framework.settings import import_from_string

from .mixins import FileContentMixin, DocStringContentMixin, MarkupProcessMixin, NoProcessMixin, SafeProcessMixin


APIDOC_DEFAULT_DOCUMENTER_CLASSES = getattr(
    settings,
    'APIDOC_DEFAULT_DOCUMENTER_CLASSES',
    ['rest_framework_apidoc.apidoc.MDDocStringsDocumenter']
)


def get_view_description(view, html=False):
    documenters = []

    if hasattr(view, 'documenter_classes'):
        for cls in view.documenter_classes:
            documenters.append(cls())
    else:
        for cls in APIDOC_DEFAULT_DOCUMENTER_CLASSES:
            documenter_class = import_from_string(cls, "APIDOC_DEFAULT_DOCUMENTER_CLASS")
            documenters.append(documenter_class())

    for documenter in documenters:
        description = documenter.get_description(view, html)
        if description:
            return description

    return ""


class Documenter(object):
    def get_description(self, view, html=True):
        if html:
            return self.process(self.get_content(view, html))
        return self.get_content(view, html)


class RSTFilesDocumenter(Documenter, FileContentMixin, MarkupProcessMixin):
    extension = ".rst"
    markup = "restructuredtext"


class RSTDocStringsDocumenter(Documenter, DocStringContentMixin, MarkupProcessMixin):
    markup = "restructuredtext"


class MDFilesDocumenter(Documenter, FileContentMixin, MarkupProcessMixin):
    extension = ".md"
    markup = "markdown"


class MDDocStringsDocumenter(Documenter, DocStringContentMixin, MarkupProcessMixin):
    markup = "markdown"


class TextileFilesDocumenter(Documenter, FileContentMixin, MarkupProcessMixin):
    extension = ".textile"
    markup = "textile"


class TextileDocStringsDocumenter(Documenter, DocStringContentMixin, MarkupProcessMixin):
    markup = "textile"


class TxtFilesDocumenter(Documenter, FileContentMixin, NoProcessMixin):
    extension = ".txt"


class TxtDocStringsDocumenter(Documenter, DocStringContentMixin, NoProcessMixin):
    pass


class HtmlFilesDocumenter(Documenter, FileContentMixin, SafeProcessMixin):
    extension = ".html"


class HtmlDocStringsDocumenter(Documenter, DocStringContentMixin, SafeProcessMixin):
    pass
