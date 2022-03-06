from django.urls import path

from . import views

app_name = "general"
urlpatterns = [
    path("states/", views.StateView.as_view(), name="states"),
]
