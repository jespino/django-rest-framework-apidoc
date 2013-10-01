from django.test import TestCase
from django.test.utils import override_settings

from rest_framework_apidoc.monkey import patch_api_view
patch_api_view()

from rest_framework.views import APIView
from rest_framework_apidoc.mixins import FileContentMixin, DocStringContentMixin

class DummyObject(object):
    pass

class RequestMock(object):
    def __init__(self, url_name):
        self._request = DummyObject()
        self._request.resolver_match = DummyObject()
        self._request.resolver_match.url_name = url_name

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
    def setUp(self):
        self.test_view = TestView.as_view()

    @override_settings(APIDOC_DOCUMENTATION_PATH="tests/test_docs")
    def test_with_extension(self):
        requestMock = RequestMock("test_with_extension")
        self.test_view.request = requestMock

        content = FileContentWithExtension().get_content(self.test_view, False)
        self.assertEqual(content, "test_with_extension\n")

        content = FileContentWithExtension().get_content(self.test_view, True)
        self.assertEqual(content, "test_with_extension\n")

    @override_settings(APIDOC_DOCUMENTATION_PATH="tests/test_docs")
    def test_without_extension(self):
        requestMock = RequestMock("test_without_extension")
        self.test_view.request = requestMock

        content = FileContentWithoutExtension().get_content(self.test_view, False)
        self.assertEqual(content, "test_without_extension\n")

        content = FileContentWithoutExtension().get_content(self.test_view, True)
        self.assertEqual(content, "test_without_extension\n")

    @override_settings(APIDOC_DOCUMENTATION_PATH="tests/test_docs")
    def test_not_existing_file(self):
        requestMock = RequestMock("test_not_existing_file")
        self.test_view.request = requestMock

        content = FileContentWithoutExtension().get_content(self.test_view, True)
        self.assertEqual(content, "")

        content = FileContentWithoutExtension().get_content(self.test_view, False)
        self.assertEqual(content, "")

class DocStringContentMixinTestCase(TestCase):
    def test_with_docstring(self):
        content = DocStringContentMixin().get_content(DocumentedTestView, True)
        self.assertEqual(content, "documented test view")

    def test_with_multiline_docstring(self):
        content = DocStringContentMixin().get_content(DocumentedMultilineTestView, True)
        self.assertEqual(content, "documented test view\nwith multiple lines\ndocumentation")

    def test_without_docstring(self):
        test_view = TestView.as_view()
        content = DocStringContentMixin().get_content(test_view, True)
        self.assertEqual(content, "")
