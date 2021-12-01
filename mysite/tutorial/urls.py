from django.urls import path, re_path

from .views import EchoView ,LogView


urlpatterns = [
    re_path(r'^fibonacci/?$', EchoView.as_view()),
    re_path(r'^logs/?$', LogView.as_view())
]
