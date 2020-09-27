from django.urls import path

from wasteline.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_profile_update,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("profile_update/", view=user_profile_update, name="profile_update",),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
