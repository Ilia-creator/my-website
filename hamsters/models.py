from django.db import models

class Hamster(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hamsters/')

    def __str__(self):
        return self.name


# Create your models here.
