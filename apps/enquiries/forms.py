from django import forms
from .models import Enquiry, NewsletterSubscriber

INPUT_CLASSES = (
    "w-full rounded-lg border border-stone-300 px-4 py-2.5 text-stone-800 "
    "focus:outline-none focus:ring-2 focus:ring-amber-600 focus:border-amber-600"
)


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone', 'email', 'company_name', 'enquiry_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'you@example.com'}),
            'company_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Company (optional)'}),
            'enquiry_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'message': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 5, 'placeholder': 'Tell us what you need...'}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'flex-1 rounded-lg border border-stone-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-600',
                'placeholder': 'Your email address'
            }),
        }
