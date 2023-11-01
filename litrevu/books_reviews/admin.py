# Register your models here.

from django.contrib import admin
from .models import (
    CustomUser,
    Book,
    Review,
    Ticket,
)


admin.site.register(CustomUser)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Ticket)
