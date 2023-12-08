from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, BookForm, TicketForm, UserProfile


def user_login(request):
    if request.user.is_authenticated:
        return redirect(to="flux")
    if request.method == "POST":
        if request.POST.get("form_submit") == "authentication":
            user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                return redirect(to="flux")
        if request.POST.get("form_submit") == "form_userprofile":
            pass
            # to implement
    return render(request, template_name="books_reviews/login.html")


@login_required(login_url="user_login")
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


@login_required(login_url="user_login")
def subscriptions(request):
    user = UserProfile.objects.get(user__username=request.user)
    data = {
        "username": user.user.username,
        "follows": enumerate(user.follows.all(), start=1),
        "followed_by": enumerate(user.followed_by.all(), start=1)
    }
    return render(request, template_name="books_reviews/subscriptions.html", context=data)


@login_required(login_url="user_login")
def my_posts(request):
    user = UserProfile.objects.get(user__username=request.user)
    personal_posts: list = list(user.tickets.all()) + list(user.reviews.all())
    data = {
        "username": user.user.username,
        "my_posts": sorted(personal_posts, key=lambda x: x.creation_date, reverse=True),
        "rating_loop": range(5)
    }
    return render(request, template_name="books_reviews/my_posts.html", context=data)


@login_required(login_url="user_login")
def creation(request):
    data: dict = {"form_book": BookForm(), "form_review": ReviewForm(), "form_ticket": TicketForm()}
    if request.method == "POST":
        if request.POST.get("form_submit") == "form_book":
            form: BookForm = BookForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data["success"] = True
                return render(request, template_name="books_reviews/creation.html", context=data)
        if request.POST.get("form_submit") == "form_review":
            form: ReviewForm = ReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.author_user = UserProfile.objects.get(user=request.user)
                new_review.save()
                data["success"] = True
                return render(request, template_name="books_reviews/creation.html", context=data)
        if request.POST.get("form_submit") == "form_ticket":
            form: TicketForm = TicketForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.author_user = UserProfile.objects.get(user=request.user)
                new_review.save()
                data["success"] = True
                return render(request, template_name="books_reviews/creation.html", context=data)
    return render(request, template_name="books_reviews/creation.html", context=data)
