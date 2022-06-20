from django import forms
from review.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs.update({'class': 'input_headline', "placeholder": " "})
        self.fields['headline'].label = "Titre"

        self.fields['body'].widget.attrs.update({'class': 'input_body', "placeholder": " "})
        self.fields['body'].label = "Description"

        self.fields['rating'].widget.attrs.update({'class': 'input_rating'})
        self.fields['rating'].label = "Note"

    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
