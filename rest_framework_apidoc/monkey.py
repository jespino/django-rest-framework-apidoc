def patch_api_view():
    from rest_framework import views

    if hasattr(views, "_patched"):
        return

    views._APIView = views.APIView
    views._patched = True

    class APIView(views.APIView):
        def get_view_description(self, html=False):
            func = self.settings.VIEW_DESCRIPTION_FUNCTION
            return func(self.__class__, html, self.request)

        @classmethod
        def as_view(cls, **initkwargs):
            view = super(views._APIView, cls).as_view(**initkwargs)
            view.cls_instance = cls(**initkwargs)
            return view

    views.APIView = APIView
