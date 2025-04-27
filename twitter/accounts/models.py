# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,Permission

class User(AbstractBaseUser):

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    create_account = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.email