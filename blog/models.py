from django.db import models
from django.db.models.fields import CharField, TextField

# Create your models here.

class Post(models.Model):
    title=CharField(max_length=150,unique=True)
    desc=TextField()

