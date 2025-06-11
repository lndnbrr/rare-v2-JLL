from django.db import models
from .category import Category

class Post(models.Model):


    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=80)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    approved = models.BooleanField(default=True)