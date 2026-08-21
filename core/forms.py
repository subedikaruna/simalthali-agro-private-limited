from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone (optional)"}),
            "message": forms.Textarea(attrs={"placeholder": "How can we help?", "rows": 5}),
        }
