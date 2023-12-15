from django.contrib.admin import register, ModelAdmin
from .models import UserProfile, Book, Review, Ticket
from django.utils.html import format_html


@register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ("user", "followers_count", "follow_count", "review_given", "ticket_opened")
    fields = ("user", "follows",)


@register(Book)
class BookAdmin(ModelAdmin):
    list_display = ("title", "author", "count_reviews", "global_rate", "has_picture")
    fields = ("title", "author", "picture")

    def global_rate(self, obj):
        try:
            return format_html(f'<span style="color: orange;">{"★" * obj.global_rate}</span>')
        except TypeError:
            return format_html("<span>-</span>")


@register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("book", "rating", "author_user", "creation_date", "ticket")
    fields = ("book", "author_user", "ticket", "headline", "bodyline", "rate")

    def rating(self, obj):
        return format_html(f'<span style="color: orange;">{'★' * obj.rate}</span>')


@register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ("book", "answered", "creation_date", "author_user", )
    fields = ("book", "author_user", "headline", "bodyline")
