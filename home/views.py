from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from product.models import *


def home(request):
    sliders = Product.objects.all().order_by('-id')[:4]
    latest = Product.objects.all().order_by('-id')[:16]
    context = {'sliders': sliders, 'latest': latest}
    return render(request, 'pages/home.html', context)


def cart(request):
    # check if the user is authenticated
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    # else:
    #     items = []
    #
    context = {}
    return render(request, 'pages/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'pages/checkout.html', context)


def account(request):
    context = {}
    return render(request, 'pages/account.html', context)


def wishlist(request):
    context = {}
    return render(request, 'pages/wish_list.html', context)


def about_us(request):
    context = {}
    return render(request, 'pages/about_us.html', context)


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message has been sent. Thanks for contact us!")
            return HttpResponseRedirect('/contactus')

    form = ContactForm
    context = {'form': form}
    return render(request, 'pages/contact_us.html', context)


def service(request):
    context = {}
    return render(request, 'pages/service.html', context)


def faq(request):
    context = {}
    return render(request, 'pages/faq.html', context)


def policy(request):
    context = {}
    return render(request, 'pages/policy.html', context)


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'pages/product_list.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id)
    context = {'product': product, 'category': category,
               'images': images, 'comments': comments,
               }
    return render(request, 'pages/product_detail.html', context)


def login(request):
    context = {}
    return render(request, 'pages/login.html', context)
