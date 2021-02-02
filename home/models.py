from django.db import models

# Create your models here.
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
