from django import forms
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """Custom form for creating users in the admin panel with required email"""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    def clean_email(self):
        """Ensure email is not empty"""
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")
        return email
