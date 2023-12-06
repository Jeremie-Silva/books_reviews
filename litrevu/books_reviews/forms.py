from django.forms import ModelForm, Textarea, Select, NumberInput
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["book", "headline", "bodyline", "rate"]
        widgets = {
            "book": Select(attrs={
                "id": "book_select",
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
            "rate": NumberInput(attrs={
                "id": "rate_input",
                "class": "form-range mb-3",
                "type": "range",
                "min": "1",
                "max": "5"
            }),
        }
