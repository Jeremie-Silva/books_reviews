from django.forms import ModelForm, Textarea, Select, RadioSelect, FileInput, PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Book, Ticket, UserProfile


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["book", "ticket", "headline", "bodyline", "rate"]
        widgets = {
            "book": Select(attrs={
                "id": "book_select",
                "class": "form-select mb-3",
                "placeholder": "",
            }),
            "ticket": Select(attrs={
                "id": "ticket_select",
                "class": "form-select mb-3",
                "placeholder": "",
            }),
            "headline": Textarea(attrs={
                "id": "headline_textarea",
                "class": "form-control mb-3",
                "placeholder": "",
                "rows": 3,
            }),
            "bodyline": Textarea(attrs={
                "id": "bodyline_textarea",
                "class": "form-control mb-3",
                "style": "height: 150px",
                "placeholder": "",
                "rows": 10,
            }),
            "rate": RadioSelect(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                attrs={
                    "id": "rate_radio"
                })
        }


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "picture"]
        widgets = {
            "title": Textarea(attrs={
                "id": "title_textarea",
                "class": "form-control mb-3",
                "placeholder": "",
                "rows": 3,
            }),
            "author": Textarea(attrs={
                "id": "author_textarea",
                "class": "form-control mb-3",
                "placeholder": "",
                "rows": 3,
            }),
            "picture": FileInput(attrs={
                "id": "picture_input",
                "class": "form-control mb-3"
            })
        }


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["book", "headline", "bodyline"]
        widgets = {
            "book": Select(attrs={
                "id": "ticket_book_select",
                "class": "form-select mb-3",
                "placeholder": "",
            }),
            "headline": Textarea(attrs={
                "id": "ticket_headline_textarea",
                "class": "form-control mb-3",
                "placeholder": "",
                "rows": 3,
            }),
            "bodyline": Textarea(attrs={
                "id": "ticket_bodyline_textarea",
                "class": "form-control mb-3",
                "style": "height: 150px",
                "placeholder": "",
                "rows": 10,
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={
                "id": "user_username",
                "class": "form-control mb-3",
                "placeholder": "",
            }),
            "password1": PasswordInput(attrs={
                "id": "user_password1",
                "placeholder": "",
            }),
            "password2": PasswordInput(attrs={
                "id": "user_password2",
                "placeholder": "",
            }),
        }
