from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import user_login, flux, subscriptions, creation, my_posts, edition, deletion


urlpatterns = [
    path("login/", user_login, name="user_login"),
    path("logout/", LogoutView.as_view(next_page="user_login"), name="logout"),

    path("", flux, name="flux"),
    path("my_posts/", my_posts, name="my_posts"),
    path("subscriptions/", subscriptions, name="subscriptions"),
    path("subscriptions/<int:user_id>/", subscriptions, name="unfollow"),
    path("creation/", creation, name="creation"),
    path("edit/<str:item>/<int:id>/", edition, name="edition"),
    path("delete/<str:item>/<int:id>/", deletion, name="deletion"),
]

