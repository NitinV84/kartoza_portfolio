from django import forms
from .models import CustomUser, UserProfile
from django.contrib.gis import forms as gis_forms


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


class UserProfileForm(forms.ModelForm):
    location = gis_forms.PointField(
        widget=gis_forms.OSMWidget(attrs={
            'map_width': 600,
            'map_height': 400,
            'default_lat': 18.153042,
            'default_lon': -0.783499,
            'default_zoom': 12,
        })
    )

    class Meta:
        model = UserProfile
        fields = ['home_address', 'phone_number', 'location']
