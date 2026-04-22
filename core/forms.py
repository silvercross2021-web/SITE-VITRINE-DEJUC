"""
Forms for DEJUC INTERNATIONAL GROUP website
"""

from django import forms
from .models import ContactMessage, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    """Formulaire de contact principal"""
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Votre prénom',
            'class': 'form-control dejuc-input',
            'id': 'contact-first-name',
        }),
        label='Prénom *'
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Votre nom de famille',
            'class': 'form-control dejuc-input',
            'id': 'contact-last-name',
        }),
        label='Nom *'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'votre@email.com',
            'class': 'form-control dejuc-input',
            'id': 'contact-email',
        }),
        label='Email *'
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+225 07 XX XX XX XX',
            'class': 'form-control dejuc-input',
            'id': 'contact-phone',
        }),
        label='Téléphone'
    )
    service = forms.ChoiceField(
        choices=ContactMessage.SERVICE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control dejuc-input dejuc-select',
            'id': 'contact-service',
        }),
        label='Service concerné'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Décrivez votre situation ou votre demande...',
            'class': 'form-control dejuc-input',
            'id': 'contact-message',
        }),
        label='Votre message *'
    )
    gdpr_consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'contact-gdpr',
        }),
        label="J'accepte que mes données soient traitées conformément à la politique de confidentialité de DEJUC International Group. *",
        error_messages={
            'required': 'Vous devez accepter notre politique de confidentialité pour envoyer votre message.'
        }
    )

    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'service', 'message', 'gdpr_consent']


class ConsultationForm(forms.Form):
    """Formulaire de demande de consultation rapide (popup/hero)"""
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Votre nom complet',
            'class': 'form-control dejuc-input',
            'id': 'consult-name',
        }),
        label='Nom complet *'
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': '+225 07 XX XX XX XX',
            'class': 'form-control dejuc-input',
            'id': 'consult-phone',
        }),
        label='Téléphone *'
    )
    service = forms.ChoiceField(
        choices=ContactMessage.SERVICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control dejuc-input',
            'id': 'consult-service',
        }),
        label='Service souhaité'
    )


class NewsletterForm(forms.ModelForm):
    """Formulaire d'inscription à la newsletter"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Votre adresse email',
            'class': 'newsletter-input',
            'id': 'newsletter-email',
        }),
        label=''
    )

    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
