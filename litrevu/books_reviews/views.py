from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, BookForm, TicketForm, CustomUserCreationForm
from .models import UserProfile, Ticket, Review
from django.contrib import messages


def user_login(request):
    data: dict = {"form_user": CustomUserCreationForm()}
    if request.user.is_authenticated:
        return redirect(to="flux")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if request.POST.get("form_submit") == "authentication":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(to="flux")
        if request.POST.get("form_submit") == "form_userprofile":
            user = User.objects.create_user(username=username, password=password)
            authenticate(request, username=username, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect("flux")
    return render(request, template_name="books_reviews/login.html", context=data)


@login_required(login_url="user_login")
def flux(request):
    user: UserProfile = UserProfile.objects.get(user__username=request.user)
    flux: list = list(user.tickets.filter(review__isnull=True)) + list(user.reviews.all())
    for user_follows in user.follows.all():
        flux += list(user_follows.tickets.filter(review__isnull=True))
        flux += list(user_follows.reviews.all())

    data = {
        "username": user.user.username,
        "flux": sorted(flux, key=lambda x: x.creation_date, reverse=True),
        "rating_loop": range(5)
    }
    return render(request, template_name="books_reviews/flux.html", context=data)


@login_required(login_url="user_login")
def subscriptions(request, user_id=None):
    user: UserProfile = UserProfile.objects.get(user__username=request.user)
    if request.method == "POST":
        if request.POST.get("form_submit") == "follow":
            user.follows.add(UserProfile.objects.get(pk=request.POST.get("others_select")))
            messages.success(request=request, message="Your changes were saved successfully.")
        if request.POST.get("form_submit") == "unfollow":
            user_to_unfollow = UserProfile.objects.get(pk=user_id)
            user.follows.remove(user_to_unfollow)
            messages.success(request=request, message="Your changes were saved successfully.")
    users_not_followed = UserProfile.objects.exclude(
        id__in=user.follows.all().values_list("id", flat=True)
    )
    users_not_followed = users_not_followed.exclude(user=request.user)
    data = {
        "username": user.user.username,
        "follows": enumerate(user.follows.all(), start=1),
        "followed_by": enumerate(user.followed_by.all(), start=1),
        "others": users_not_followed,
    }
    return render(request, template_name="books_reviews/subscriptions.html", context=data)


@login_required(login_url="user_login")
def my_posts(request):
    user: UserProfile = UserProfile.objects.get(user__username=request.user)
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
                messages.success(request=request, message="Your changes were saved successfully.")
                return render(request, template_name="books_reviews/creation.html", context=data)
        if request.POST.get("form_submit") == "form_review":
            form: ReviewForm = ReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.author_user = UserProfile.objects.get(user=request.user)
                new_review.save()
                messages.success(request=request, message="Your changes were saved successfully.")
                return render(request, template_name="books_reviews/creation.html", context=data)
        if request.POST.get("form_submit") == "form_ticket":
            form: TicketForm = TicketForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.author_user = UserProfile.objects.get(user=request.user)
                new_review.save()
                messages.success(request=request, message="Your changes were saved successfully.")
                return render(request, template_name="books_reviews/creation.html", context=data)
    if request.GET.get("id"):
        ticket_related: Ticket = Ticket.objects.get(pk=request.GET.get("id"))
        data["form_review"] = ReviewForm(instance=Review(book=ticket_related.book, ticket=ticket_related))
        render(request, template_name="books_reviews/creation.html", context=data)
    return render(request, template_name="books_reviews/creation.html", context=data)


@login_required(login_url="user_login")
def edition(request, item, id):
    if request.method == "POST":
        if item == "ticket" and request.user == Ticket.objects.get(pk=id).author_user.user:
            form: TicketForm = TicketForm(request.POST, instance=Ticket.objects.get(pk=id))
            if form.is_valid():
                form.save()
                messages.success(request=request, message="Your changes were saved successfully.")
                return redirect("my_posts")
        if item == "review" and request.user == Review.objects.get(pk=id).author_user.user:
            form: ReviewForm = ReviewForm(request.POST, instance=Review.objects.get(pk=id))
            if form.is_valid():
                form.save()
                messages.success(request=request, message="Your changes were saved successfully.")
                return redirect("my_posts")
    if item == "ticket":
        data: dict = {"form_ticket": TicketForm(instance=Ticket.objects.get(pk=id)), "item": "ticket"}
    elif item == "review":
        data: dict = {"form_review": ReviewForm(instance=Review.objects.get(pk=id)), "item": "review"}
    else:
        data: dict = {}
    return render(request, template_name="books_reviews/edition.html", context=data)


@login_required(login_url="user_login")
def deletion(request, item, id):
    if request.method == "POST":
        if item == "ticket" and request.user == Ticket.objects.get(pk=id).author_user.user:
            try:
                Ticket.objects.get(pk=id).delete()
                messages.success(request=request, message="Your changes were saved successfully.")
            except:
                messages.error(request=request, message="This item is protected.")
        if item == "review" and request.user == Review.objects.get(pk=id).author_user.user:
            try:
                Review.objects.get(pk=id).delete()
                messages.success(request=request, message="Your changes were saved successfully.")
            except:
                messages.error(request=request, message="This item is protected.")
    return redirect("my_posts")
