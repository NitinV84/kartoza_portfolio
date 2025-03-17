from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as geomodels


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    location = geomodels.PointField()
    
    def __str__(self):
        return self.user.username
