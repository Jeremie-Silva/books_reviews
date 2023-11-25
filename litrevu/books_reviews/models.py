from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    follows = models.ManyToManyField(to="self", symmetrical=False, related_name='followed_by')
    is_staff = False

    @property
    def followers_count(self):
        return self.followed_by.count()

    @property
    def follow_count(self):
        return self.follows.count()

    @property
    def review_given(self):
        return self.reviews.count()

    @property
    def ticket_opened(self):
        return self.tickets.count()

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    picture = models.ImageField(
        upload_to="books_reviews/static/books_reviews/uploads/%Y/%m/%d/", validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])
        ]
    )

    @property
    def global_rate(self):
        return self.reviews.all().aggregate(models.Avg("rate"))["rate__avg"] or None

    @admin.display(boolean=True)
    def has_picture(self):
        return True if self.picture else False

    @property
    def count_reviews(self):
        return len(self.reviews.all())

    def __str__(self):
        return self.title


class Ticket(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="tickets")
    author_user = models.ForeignKey(to=UserProfile, on_delete=models.PROTECT, related_name="tickets")
    headline = models.CharField(max_length=150)
    bodyline = models.CharField(max_length=3000, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    @admin.display(boolean=True)
    def answered(self):
        return True if self.review else False

    def __str__(self):
        return self.book.title


class Review(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="reviews")
    author_user = models.ForeignKey(to=UserProfile, on_delete=models.PROTECT, related_name="reviews")
    ticket = models.OneToOneField(
        to=Ticket, on_delete=models.PROTECT, related_name="review", null=True, blank=True
    )
    headline = models.CharField(max_length=150)
    bodyline = models.CharField(max_length=8000, blank=True)
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} > {self.author_user} > {self.rate}"
