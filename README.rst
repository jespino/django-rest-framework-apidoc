Django REST Framework APIDoc
============================

Library to better documentation system for Django REST framework.

This support file based documentation and other markup languages like RestructuredText or Textile.

Configuration
-------------

To configure apidoc in djangorestframework version <= 2.3.8, you need to monkey
patch it. Add this line in a very first loaded models module

.. code:: python
  from rest_framework_apidoc.monkey import patch_api_view; patch_api_view()

Then you have to configure your `VIEW_DESCRIPTION_FUNCTION` of `REST_FRAMEWORK`
setting to use the rest_framework_apidoc version:

.. code:: python
  REST_FRAMEWORK = {
      ...,
      'VIEW_DESCRIPTION_FUNCTION': 'rest_framework_apidoc.apidoc.get_view_description',
      ...,
  }

Then you can configure your apidoc default documenter classes:

.. code:: python
  APIDOC_DEFAULT_DOCUMENTER_CLASSES = ['rest_framework_apidoc.apidoc.MDDocStringDocumenter']

The `APIDOC_DEFAULT_DOCUMENTER_CLASSES` default value is `['rest_framework_apidoc.apidoc.MDDocStringsDocumenter']`

If you use file based documentation, you can set the path to your documentation files:

You can override the default setting for a APIView adding the attribute `documenter_classes`.

.. code:: python
  APIDOC_DOCUMENTATION_PATH = "my-api-documentation"

The `APIDOC_DOCUMENTATION_PATH` default value is `apidoc`

APIDoc Mixins
-------------

The documenter classes are composed by 2 types of mixings, the content mixins
and the process mixins. The content mixins obtain the documentation text, and
the process mixing transform this text in another thing.

Content mixins
~~~~~~~~~~~~~~

* **FileContentMixin**: Get the content from a file named like the url_name +
  extension attribute of the class (if exists), and placed in the
  `APIDOC_DOCUMENTATION_PATH`.
* **DocStringContentMixin**: Get the content from the APIView doc string.

Process mixins
~~~~~~~~~~~~~~

* **MarkupProcessMixin**: Use django-markup to convert to html the content, based
  on the markup class attribute.
* **NoProcessMixin**: Do nothing
* **SafeProcessMixin**: Mark as safe the content.

Documenter Classes
------------------

RSTFilesDocumenter
~~~~~~~~~~~~~~~~~~
Composed by FileContentMixin and MarkupProcessMixin with extension = ".rst" and markup = "restructuredtext"

RSTDocStringsDocumenter
~~~~~~~~~~~~~~~~~~~~~~~
Composed by DocStringContentMixin and MarkupProcessMixin with markup = "restructuredtext"

MDFilesDocumenter
~~~~~~~~~~~~~~~~~
Composed by FileContentMixin and MarkupProcessMixin with extension = ".md" and markup = "markdown"

MDDocStringsDocumenter
~~~~~~~~~~~~~~~~~~~~~~
Composed by DocStringContentMixin and MarkupProcessMixin with markup = "markdown"

TextileFilesDocumenter
~~~~~~~~~~~~~~~~~~~~~~
Composed by FileContentMixin and MarkupProcessMixin with extension = ".textile" and markup = "textile"

TextileDocStringsDocumenter
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Composed by DocStringContentMixin and MarkupProcessMixin with markup = "textile"

TxtFilesDocumenter
~~~~~~~~~~~~~~~~~~
Composed by FileContentMixin and NoProcessMixin with extension = ".txt"

TxtDocStringsDocumenter
~~~~~~~~~~~~~~~~~~~~~~~
Composed by DocStringContentMixin and NoProcessMixin

HtmlFilesDocumenter
~~~~~~~~~~~~~~~~~~~
Composed by FileContentMixin, SafeProcessMixin with extension = ".html"

HtmlDocStringsDocumenter
~~~~~~~~~~~~~~~~~~~~~~~~
Composed by DocStringContentMixin and SafeProcessMixin
