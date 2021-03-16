from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView


from home.models import ContactMessage
from .models import *



# Create your views here.

def index(request):
    return HttpResponse("My Product Page")


def add_comment(request, p_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.rate = form.cleaned_data['rate']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = p_id
            user_name = request.user
            data.users_id = user_name.id
            data.save()
            messages.success(request, "Your review has been sent. Thanks for your review!")
            return HttpResponseRedirect(url)
    return HttpResponse(url)
