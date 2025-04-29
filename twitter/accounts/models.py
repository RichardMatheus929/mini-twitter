# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager

class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    create_account = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    is_active = models.BooleanField(default=True, help_text="Campo padrão necessário para o Django admin")
    is_staff = models.BooleanField(default=False, help_text="Campo padrão necessário para o Django admin")

    def __str__(self) -> str:
        return self.email