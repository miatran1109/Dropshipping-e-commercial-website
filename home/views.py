from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from .models import *
from product.models import *


def home(request):
    sliders = Product.objects.all().order_by('-id')[:4]
    context = {'sliders': sliders}
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
    context = {}
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
    context = {'products': products}
    return render(request, 'pages/product_list.html', context)


def product_detail(request):
    context = {}
    return render(request, 'pages/product_detail.html', context)


def login(request):
    context = {}
    return render(request, 'pages/login.html', context)
