from django.urls import path
from .views import user_login, flux, subscriptions, creation, my_posts


urlpatterns = [
    path("login/", user_login, name="user_login"),
    path("", flux, name="flux"),
    path("my_posts/", my_posts, name="my_posts"),
    path("subscriptions/", subscriptions, name="subscriptions"),
    path("creation/", creation, name="creation"),
]
