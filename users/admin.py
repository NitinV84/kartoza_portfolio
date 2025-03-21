from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.gis import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import CustomUserCreationForm
from .models import CustomUser, UserProfile


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
        """Override save to send an invitation email when a new user is created."""
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

            # Render HTML email template
            context = {
                "full_name": obj.get_full_name(),
                "reset_link": reset_link,
                "username": obj.username,
            }
            html_content = render_to_string("emails/invitation_email.html", context)

            # Send email
            email = EmailMultiAlternatives(
                subject="You're invited to our platform",
                body=f"Hello {obj.get_full_name()},\n\nYou've been registered by an admin.\n"
                f"Please set your password using this link: {reset_link}\n\nThank you!",
                from_email=settings.EMAIL_HOST_USER,
                to=[obj.email],
            )
            email.attach_alternative(html_content, "text/html")  # Attach HTML content
            email.send()


@admin.register(UserProfile)
class UserProfileAdmin(admin.GISModelAdmin):
    list_display = ["id", "user", "location", "home_address"]


admin.site.register(CustomUser, CustomUserAdmin)
