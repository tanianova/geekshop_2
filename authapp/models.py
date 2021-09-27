from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar',blank=True)
    # age=models.PositiveSmallIntegerField(blank=True,null=True)
    age=models.PositiveSmallIntegerField(verbose_name='возраст',default=18)
    language = models.CharField(max_length=3,default='EN')