from django.urls import path

from . import views

app_name = "general"
urlpatterns = [
    path("states/", views.StateView.as_view(), name="states"),
    path("states/<int:pk>/", views.StateDetailView.as_view(), name="states-details"),
    path("districts/", views.DistrictView.as_view(), name="districts"),
    path(
        "districts/<int:pk>/",
        views.DistrictDetailView.as_view(),
        name="districts-details",
    ),
    path("professions/", views.ProfessionView.as_view(), name="professions"),
    path(
        "professions/<int:pk>/",
        views.ProfessionDetailView.as_view(),
        name="professions-details",
    ),
]
