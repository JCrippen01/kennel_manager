from django.urls import path
from .views import (
    register_user,
    login_user,
    logout_user,
    get_user_profile,
    update_profile,
    admin_dashboard,
    staff_dashboard,
    customer_dashboard,
    list_users,
    update_user_role,
    delete_user,
)

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("profile/", get_user_profile, name="profile"),
    path("profile/update/", update_profile, name="profile-update"),
    path("dashboard/admin/", admin_dashboard, name="admin-dashboard"),
    path("dashboard/staff/", staff_dashboard, name="staff-dashboard"),
    path("dashboard/customer/", customer_dashboard, name="customer-dashboard"),
    # ✅ Fix: Remove extra `users/` prefix
    path("", list_users, name="list-users"),
    path("<int:user_id>/", update_user_role, name="update-user-role"),
    path("<int:user_id>/delete/", delete_user, name="delete-user"),
]
