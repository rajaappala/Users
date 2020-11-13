from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class CustomUser(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(
        max_length=32,
        unique=True,
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9,;,_]*$', message="Username is invalid")])
    email = models.EmailField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self):
        return self.username
