from django.urls import include, path
from accounts import views

app_name = "accounts"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("edit-profile/", views.edit_user_profile, name="edit_profile"),
]
