from django.urls import path
from . import views


urlpatterns = [
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path(
        "profile/edit/<int:pk>/", views.EditProfileView.as_view(), name="edit_profile"
    ),
]
