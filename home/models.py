from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, forms, TextInput


class ContactMessage(models.Model):
    name = models.CharField(blank=True, max_length=50)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=50)
    ip = models.CharField(blank=True, max_length=50)
    note = models.CharField(blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = {'name', 'subject', 'email', 'message'}


class AccountManager(PermissionsMixin):
    object = BaseUserManager()

    class Meta:
        abstract = True

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Username cannot be empty')
        if email is None:
            raise TypeError('Email cannot be empty')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_super_user(self, username, email, password=None):
        if password is None:
            raise TypeError('Password cannot be empty')

        user = self.create_user(username, email, password)
        user.is_super_user = True
        user.is_admin = True
        user.save()
        return user


class Account(AbstractBaseUser):
    username = models.CharField('settings.AUTH_USER_MODEL', max_length=300, unique=True)
    email = models.EmailField(max_length=300, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # only for superuser
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def tokens(self):
        return ''