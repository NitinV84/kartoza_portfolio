import json

from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, UpdateView

from .forms import UserProfileForm
from .models import CustomUser, UserProfile


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
        messages.error(
            self.request, "Username or password is incorrect. Please try again."
        )
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

        messages.success(
            self.request, "Your password has been set. You can now log in."
        )
        return redirect("login")


class ProfileView(LoginRequiredMixin, ListView):
    """
    Profile view that displays the user's profile.

    Attributes:
        model (UserProfile): The model to be displayed.
        template_name (str): The template used to render the profile page.
        context_object_name (str): The context variable name for the user profile.
    """

    model = UserProfile
    template_name = "users/profile.html"
    context_object_name = "profile"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return super().get_queryset().get(user=self.request.user)


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    View to allow authenticated users to edit only their own profile.

    Attributes:
        model (UserProfile): The model associated with this view.
        form_class (UserProfileForm): The form used to edit the user's profile.
        template_name (str): The template used to render the edit profile page.
        context_object_name (str): The name of the context object in the template.
        success_url (str): The URL to redirect to after a successful profile update.
    """

    model = UserProfile
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    context_object_name = "profile"
    success_url = reverse_lazy("profile")

    def dispatch(self, request, *args, **kwargs):
        """Ensure that users can only edit their own profiles."""
        profile = get_object_or_404(UserProfile, pk=self.kwargs["pk"])

        if profile.user != self.request.user:
            return HttpResponse("You are not allowed to edit this profile.", status=403)

        return super().dispatch(request, *args, **kwargs)


@method_decorator(staff_member_required, name='dispatch')
class UserMapView(UserPassesTestMixin, TemplateView):
    """
    Class-based view to display a full-screen map with all registered users' locations.
    Only admin users can access this page.
    """

    template_name = "users/map.html"

    def test_func(self):
        """Allow only admin users to access the map."""
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Return a Forbidden response if the user is not an admin."""
        return HttpResponseForbidden("You are not allowed to view this page.")

    def get_context_data(self, **kwargs):
        """Pass user locations as JSON data to the template."""
        context = super().get_context_data(**kwargs)

        # Add admin context for the sidebar
        context.update(admin.site.each_context(self.request))
        users = UserProfile.objects.exclude(location=None)

        users_data = []
        for user in users:
            users_data.append(
                {
                    "type": "Feature",
                    "geometry": (
                        json.loads(user.location.geojson) if user.location else None
                    ),
                    "properties": {
                        "username": user.user.username,
                        "first_name": user.user.first_name,
                        "last_name": user.user.last_name,
                        "email": user.user.email,
                        "home_address": user.home_address or "N/A",
                        "phone_number": (
                            str(user.phone_number) if user.phone_number else "N/A"
                        ),
                    },
                }
            )

        context["users_json"] = json.dumps(
            {"type": "FeatureCollection", "features": users_data}
        )
        return context
