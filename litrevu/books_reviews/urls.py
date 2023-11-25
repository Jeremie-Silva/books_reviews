from django.urls import path
from .views import (
    login,
    inscription,
    flux,
    subscriptions,
    ticket_creation,
    review_creation,
    my_posts
)


urlpatterns = [
    path("login/", login, name="login"),
    path("inscription/", inscription, name="inscription"),
    path("", flux, name="flux"),
    path("my_posts/", my_posts, name="my_posts"),
    path("subscriptions/", subscriptions, name="subscriptions"),
    path("ticket_creation/", ticket_creation, name="ticket_creation"),
    path("review_creation/", review_creation, name="review_creation"),
]
