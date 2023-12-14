from django.contrib.admin import register, ModelAdmin
from .models import UserProfile, Book, Review, Ticket


@register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ("user", "followers_count", "follow_count", "review_given", "ticket_opened")
    fields = ("user", "follows",)


@register(Book)
class BookAdmin(ModelAdmin):
    list_display = ("title", "count_reviews", "author", "global_rate", "has_picture")
    fields = ("title", "author", "picture")


@register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("book", "rate", "author_user", "creation_date", "ticket")
    fields = ("book", "author_user", "ticket", "headline", "bodyline", "rate")


@register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ("book", "answered", "creation_date", "author_user", )
    fields = ("book", "author_user", "headline", "bodyline")
