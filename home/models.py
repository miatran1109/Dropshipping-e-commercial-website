from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.forms import ModelForm, forms, TextInput
from django.utils.translation import ugettext_lazy as _


# User model
class AccountManager(BaseUserManager):
    # object = BaseUserManager()

    class Meta:
        abstract = True

    def create_user(self, email,salt, password=None, **extra_fields):
        if email is None:
            raise TypeError('Email cannot be empty')
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(email = email,salt = salt, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,salt, password=None, **extra_fields):

        #Create and save a SuperUser with the given email and password.

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email,salt, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('settings.AUTH_USER_MODEL', max_length=300, unique=True)
    email = models.EmailField(max_length=300, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # only for superuser
    salt = models.CharField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','salt','password']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def tokens(self):
        return ''

class Token(models.Model):
    userID = models.IntegerField(blank = False)
    token = models.CharField(blank = False, max_length = 5000)
    created_at = models.DateTimeField(auto_now_add = True)


class Order(models.Model):
    first_name = models.CharField(blank = False, max_length = 5000)
    last_name = models.CharField(blank = False, max_length = 5000)
    address = models.CharField(blank = False, max_length = 5000)
    city = models.CharField(blank = False, max_length = 5000)
    district = models.CharField(blank = False, max_length = 5000)
    phone = models.IntegerField(blank = False)
    email = models.EmailField(blank = False, max_length = 5000)
    note = models.CharField(blank = None, max_length = 10000)


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
