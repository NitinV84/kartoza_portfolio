from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models as geomodels


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Attributes:
        email (EmailField): The unique email address of the user.
    """
    email = models.EmailField(unique=True)

    def __str__(self):
        """Returns the username of the user."""
        return self.username


class UserProfile(models.Model):
    """
    User profile model extending the CustomUser model.
    
    Attributes:
        user (OneToOneField): A one-to-one relationship with CustomUser.
        home_address (TextField): The home address of the user.
        phone_number (CharField): The phone number of the user.
        location (PointField): The geographic location of the user.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    home_address = models.TextField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    location = geomodels.PointField(null=True)

    def __str__(self):
        """Returns the username of the associated user."""
        return self.user.username
