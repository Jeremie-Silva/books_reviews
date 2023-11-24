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
    data = {
        "tickets": user.tickets.all(),
        "reviews": user.reviews.all()
    }
    return render(request, template_name="books_reviews/flux.html", context=data)


@login_required(login_url="login")
def subscriptions(request):
    user = UserProfile.objects.get(user__username=request.user)
    data = {
        "username": user.user.username,
        "follows": user.follows.all(),
        "followed_by": user.followed_by.all()
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
    data = {
        "tickets": user.tickets.all(),
        "reviews": user.reviews.all()
    }
    return render(request, template_name="books_reviews/my_posts.html", context=data)
