from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("refresh_token", views.RefreshTokenView.as_view(), name="refresh_token"),
    path("test", views.TestingView.as_view(), name="test_view"),
]
