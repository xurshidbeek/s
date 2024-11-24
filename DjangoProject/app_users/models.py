from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import MyUserManager as UserManager

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profile_images')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    def __str__(self):
        return self.email

