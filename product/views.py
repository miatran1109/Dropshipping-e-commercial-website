from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from home.models import ContactMessage
from .models import *


# Create your views here.
def index(request):
    return HttpResponse("My Product Page")