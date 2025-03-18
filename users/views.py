from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import UserProfile, CustomUser
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib import messages
from django.contrib.auth.views import LoginView


class UserLoginView(LoginView):
    """
    Custom login view that extends Django's built-in LoginView.

    Attributes:
        template_name (str): The template used for rendering the login page.
    
    Methods:
        get_success_url(): Redirects the user to their profile page after successful login.
    """
    template_name = "users/login.html"

    def form_invalid(self, form):
        """
        Called when login form is invalid (wrong username/password).
        Adds an error message and re-renders the login page.
        """
        messages.error(self.request, "Username or password is incorrect. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect the user after a successful login.
        
        Displays a success message and redirects the user to their profile page.
        """
        return reverse_lazy("profile")


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
        return redirect('login')


class ProfileView(LoginRequiredMixin, ListView):
    """
    Profile view that displays the user's profile.

    Attributes:
        model (UserProfile): The model to be displayed.
        template_name (str): The template used to render the profile page.
        context_object_name (str): The context variable name for the user profile.
    """
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return super().get_queryset().get(user = self.request.user)
