from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Enter an email')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_admin=True,
            is_active=True,
            is_superuser=True,
            is_staff=True,

            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Enter an email')

        user = self.model(username=username, email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=60, unique=True, db_index=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to="profile_images", default="blank-profile-picture.png")
    bio = models.TextField(max_length=150, null=True, blank=True)

    # user status
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    following = models.ManyToManyField("self", symmetrical=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username


