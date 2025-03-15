from django import forms

from core.models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Contact Name",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Email Address",
            }
        )
    )

    class Meta:
        model = Contact
        fields = ("name", "email")
