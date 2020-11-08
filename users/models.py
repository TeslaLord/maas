from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=2000)
    skills = models.CharField(max_length=2000)
    aoi = models.CharField(max_length=2000)

    def __str__(self):
        return f'{self.user.username} Profile'
