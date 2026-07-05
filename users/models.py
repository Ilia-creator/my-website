from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=30, blank=True, verbose_name='Phone')

    def __str__(self):
        return self.username
