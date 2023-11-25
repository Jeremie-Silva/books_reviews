from django.contrib import admin
from .models import (
    UserProfile,
    Book,
    Review,
    Ticket,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "followers_count", "follow_count", "review_given", "ticket_opened")
    fields = ("user", "follows")


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "count_reviews", "author", "global_rate", "has_picture")
    fields = ("title", "author", "picture")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "rate", "author_user", "creation_date", "ticket")
    fields = ("book", "author_user", "ticket", "headline", "bodyline", "rate")


class TicketAdmin(admin.ModelAdmin):
    list_display = ("book", "answered", "creation_date", "author_user", )
    fields = ("book", "author_user", "headline", "bodyline")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Ticket, TicketAdmin)
