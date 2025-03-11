from django.urls import path
from .views import (
    register_user,
    login_user,
    logout_user,
    get_user_profile,
    update_profile,
)


urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("profile/", get_user_profile, name="profile"),
    path("profile/update/", update_profile, name="profile-update"),
]
