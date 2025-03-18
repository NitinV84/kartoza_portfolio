from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import CustomUser, UserProfile
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "first_name", "last_name", "password"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Override save to send invitation email when a new user is created."""
        is_new_user = not obj.pk  # Check if user is newly created
        if is_new_user and obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

        if is_new_user:

            # Create user profile
            UserProfile.objects.get_or_create(user=obj)
            # Generate a valid password reset token
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            token = default_token_generator.make_token(obj)

            # Correct password reset link
            reset_link = request.build_absolute_uri(
                reverse(
                    "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
                )
            )

            subject = "You're invited to our platform"
            message = f"Hello {obj.get_full_name()},\n\nYou've been registered by an admin.\nPlease click the link below to set your password:\n{reset_link}\n\nThank you!"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email])


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
