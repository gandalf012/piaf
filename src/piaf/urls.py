from django.urls import path, re_path

from .views import (
    IndexView,
    AdminView,
    AdminDatasetView,
    ParagraphView,
    QuestionView,
    get_datasets_info,
)
from .apis import MeView


app_name = "app"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin", AdminView.as_view(), name="admin"),
    path("admin/dataset", AdminDatasetView.as_view(), name="dataset"),
    path("api/datasets", get_datasets_info),
    path("api/paragraph", ParagraphView.as_view(), name="api_paragraph"),
    path("api/question", QuestionView.as_view(), name="api_question"),
    path("me", MeView.as_view(), name="me"),
    re_path(r'^.*$', IndexView.as_view(), name="index"),
]
