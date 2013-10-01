from django.test import TestCase
from django.test.utils import override_settings

from rest_framework.views import APIView
from rest_framework_apidoc.mixins import FileContentMixin, DocStringContentMixin


class DummyObject(object):
    pass


class RequestMock(object):
    def __init__(self, url_name):
        self.resolver_match = DummyObject()
        self.resolver_match.url_name = url_name


class TestView(APIView):
    pass


class DocumentedTestView(APIView):
    "documented test view"


class DocumentedMultilineTestView(APIView):
    """documented test view
    with multiple lines
    documentation"""


class FileContentWithExtension(FileContentMixin):
    extension = ".extension"


class FileContentWithoutExtension(FileContentMixin):
    pass


class FileContentMixinTestCase(TestCase):
    @override_settings(APIDOC_DOCUMENTATION_PATH="tests/test_docs")
    def test_with_extension(self):
        requestMock = RequestMock("test_with_extension")

        content = FileContentWithExtension().get_content(TestView, False, requestMock)
        self.assertEqual(content, "test_with_extension\n")

        content = FileContentWithExtension().get_content(TestView, True, requestMock)
        self.assertEqual(content, "test_with_extension\n")

    @override_settings(APIDOC_DOCUMENTATION_PATH="tests/test_docs")
    def test_without_extension(self):
        requestMock = RequestMock("test_without_extension")

        content = FileContentWithoutExtension().get_content(TestView, False, requestMock)
        self.assertEqual(content, "test_without_extension\n")

        content = FileContentWithoutExtension().get_content(TestView, True, requestMock)
        self.assertEqual(content, "test_without_extension\n")

    @override_settings(APIDOC_DOCUMENTATION_PATH="tests/test_docs")
    def test_not_existing_file(self):
        requestMock = RequestMock("test_not_existing_file")

        content = FileContentWithoutExtension().get_content(TestView, True, requestMock)
        self.assertEqual(content, "")

        content = FileContentWithoutExtension().get_content(TestView, False, requestMock)
        self.assertEqual(content, "")


class DocStringContentMixinTestCase(TestCase):
    def test_with_docstring(self):
        content = DocStringContentMixin().get_content(DocumentedTestView, True)
        self.assertEqual(content, "documented test view")

    def test_with_multiline_docstring(self):
        content = DocStringContentMixin().get_content(DocumentedMultilineTestView, True)
        self.assertEqual(content, "documented test view\nwith multiple lines\ndocumentation")

    def test_without_docstring(self):
        content = DocStringContentMixin().get_content(TestView, True)
        self.assertEqual(content, "")
