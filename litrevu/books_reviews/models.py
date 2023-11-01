# Create your models here.

from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator
)
from django.contrib.auth.models import AbstractUser


class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    picture = models.ImageField(
        upload_to="uploads/%Y/%m/%d/", validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])
        ]
    )

    @property
    def global_rate(self):
        return self.reviews.all().aggregate(models.Avg("rate"))["rate__avg"] or None


class CustomUser(AbstractUser):
    following = models.ManyToManyField(
        to="self", symmetrical=False, related_name="followers", blank=True
    )


class Review(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="reviews")
    author_user = models.ForeignKey(to=CustomUser, on_delete=models.PROTECT, related_name="reviews")
    headline = models.CharField(max_length=150)
    bodyline = models.CharField(max_length=8000, blank=True)
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    creation_date = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="tickets")
    author_user = models.ForeignKey(to=CustomUser, on_delete=models.PROTECT, related_name="tickets")
    response = models.OneToOneField(
        to=Review, on_delete=models.PROTECT, related_name="ticket", null=True, blank=True
    )
    answered = models.BooleanField(default=False)
    headline = models.CharField(max_length=150)
    bodyline = models.CharField(max_length=3000, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.answered = True if self.response is not None else False
        super().save(*args, **kwargs)
