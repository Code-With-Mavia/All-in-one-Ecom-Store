from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_last_name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_profile_picture'}),
        }

class ChangeEmailForm(forms.ModelForm):
    new_email = forms.EmailField(label="New Email", required=True)
    confirm_email = forms.EmailField(label="Confirm New Email", required=True)

    class Meta:
        model = User
        fields = ['new_email', 'confirm_email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_email'].widget.attrs.update({'class': 'form-control', 'id': 'id_new_email'})
        self.fields['confirm_email'].widget.attrs.update({'class': 'form-control', 'id': 'id_confirm_email'})

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get("new_email")
        confirm_email = cleaned_data.get("confirm_email")

        if new_email and confirm_email and new_email != confirm_email:
            raise ValidationError("Emails do not match.")

        if User.objects.filter(email=new_email).exists():
            raise ValidationError("This email is already in use.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["new_email"]
        if commit:
            user.save()
        return user

class DeleteAccountForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="I confirm I want to delete my account"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['confirm'].widget.attrs.update({'class': 'form-check-input', 'id': 'id_confirm'})

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("confirm"):
            raise ValidationError("You must confirm to delete your account.")
        return cleaned_data
