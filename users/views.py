from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib import messages
from django.http import HttpResponse


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom password reset confirmation view.

    Methods:
        form_valid(form): Handles the password reset process and updates the user profile.
    """

    def form_valid(self, form):
        """
        Handles the form submission for resetting a password.

        - Sets the new password for the user.
        - Ensures the password is hashed before saving.
        - Redirects the user to the login page with a success message.

        Args:
            form (PasswordResetConfirmForm): The form containing the new password.

        Returns:
            HttpResponseRedirect: Redirects to the login page after successful password reset.
        """
        user = form.user
        user.set_password(form.cleaned_data["new_password1"])
        user.save()

        # Retrieve user profile and clear invite token
        custom_user = CustomUser.objects.get(username=user.username)
        custom_user.save()

        messages.success(self.request, "Your password has been set. You can now log in.")
        return HttpResponse("Your password has been set. You can now log in.")
