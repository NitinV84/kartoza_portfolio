from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver


def log_auth_event(user, action_message):
    """Logs user login/logout events as separate admin actions."""
    LogEntry.objects.create(
        user=user,
        content_type=ContentType.objects.get_for_model(user),
        object_id=user.pk,
        object_repr=f"{user.username} ({user.email})",  # Show clear user info
        action_flag=ADDITION,  # Log as a new event instead of a model update
        change_message=action_message,  # Store login/logout message
    )


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    log_auth_event(user, "User logged in")


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    log_auth_event(user, "User logged out")
