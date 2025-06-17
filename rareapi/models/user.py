from django.db import models


class User (models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200)
    profile_image_url = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()
    is_staff = models.BooleanField()
    uid = models.CharField(max_length=100, unique=True)
