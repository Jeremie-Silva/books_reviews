from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import UserProfile


def login(request):
    if request.user.is_authenticated:
        return redirect(to="flux")
    return render(request, template_name="books_reviews/login.html")


def inscription(request):
    if request.user.is_authenticated:
        return redirect(to="flux")
    return render(request, template_name="books_reviews/inscription.html")


@login_required(login_url="login")
def flux(request):
    user = UserProfile.objects.get(user__username=request.user)
    flux: list = []
    for user_follows in user.follows.all():
        flux += list(user_follows.tickets.all())
        flux += list(user_follows.reviews.all())
    data = {
        "username": user.user.username,
        "flux": sorted(flux, key=lambda x: x.creation_date, reverse=True),
        "rating_loop": range(5)
    }
    return render(request, template_name="books_reviews/flux.html", context=data)


@login_required(login_url="login")
def subscriptions(request):
    user = UserProfile.objects.get(user__username=request.user)
    data = {
        "username": user.user.username,
        "follows": enumerate(user.follows.all(), start=1),
        "followed_by": enumerate(user.followed_by.all(), start=1)
    }
    return render(request, template_name="books_reviews/subscriptions.html", context=data)


@login_required(login_url="login")
def ticket_creation(request):
    return render(request, template_name="books_reviews/ticket_creation.html")


@login_required(login_url="login")
def review_creation(request):
    return render(request, template_name="books_reviews/review_creation.html")


@login_required(login_url="login")
def my_posts(request):
    user = UserProfile.objects.get(user__username=request.user)
    personal_posts: list = list(user.tickets.all()) + list(user.reviews.all())
    data = {
        "username": user.user.username,
        "my_posts": sorted(personal_posts, key=lambda x: x.creation_date, reverse=True),
        "rating_loop": range(5)
    }
    return render(request, template_name="books_reviews/my_posts.html", context=data)
