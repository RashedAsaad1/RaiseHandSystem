from django.db import models

# Create your models here.


class Login(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class group(models.Model):
    name = models.CharField(max_length=30)
    msg = models.CharField(max_length=255)  # or any other field type
    timestamp = models.DateTimeField(auto_now_add=True)
    retracted = models.BooleanField(default=False)
    groupcode = models.CharField(max_length=40)
    def __str__(self):
        return self.name



