from django import forms

from sandbox.models import Contact, Rating, Restaurant


class ContactForm(forms.ModelForm):
    """Form for creating and updating contacts."""

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Contact Name",
                "class": "input input-bordered w-full",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "input input-bordered w-full",
            }
        )
    )

    class Meta:
        model = Contact
        fields = ["name", "email"]


class RestaurantForm(forms.ModelForm):
    """Form for creating and updating restaurants."""

    class Meta:
        model = Restaurant
        fields = ("name", "latitude", "longitude")


class RatingForm(forms.ModelForm):
    """Form for creating and updating ratings."""

    class Meta:
        model = Rating
        fields = ("restaurant", "user", "rating")
