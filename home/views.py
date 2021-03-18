from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate
import bcrypt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models.expressions import RawSQL
from .serializers import AccountRegisterSerializer, OrderSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import connection
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
import jwt
from datetime import datetime

from rest_framework.renderers import TemplateHTMLRenderer

from .models import *
from product.models import *


def home(request):
    category = Category.objects.all()
    sliders = Slider.objects.all()
    latest = Product.objects.all().order_by('-id')[:16]
    context = {'sliders': sliders, 'latest': latest, 'category': category}
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
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/cart.html', context)


def checkout(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/checkout.html', context)


def token_check(user_token):

    check_obj = Token.objects.filter(
        id__in=RawSQL('SELECT id FROM home_token WHERE token = %s', [user_token]))
    check_value = check_obj.values()
    check_token = check_value[0]['token']

    if check_token == user_token:
        return True
    else:
        return False



def account(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/account.html', context)


def wishlist(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/wish_list.html', context)


def about_us(request):
    category = Category.objects.all()
    context = {'category': category}
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
    category = Category.objects.all()
    context = {'form': form, 'category': category}
    return render(request, 'pages/contact_us.html', context)


def service(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/service.html', context)


def faq(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/faq.html', context)


def policy(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/policy.html', context)


def product_list(request):
    category = Category.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'category': category}
    return render(request, 'pages/product_list.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id).order_by('-id')
    context = {'product': product, 'category': category,
               'images': images, 'comments': comments,
               }

    return render(request, 'pages/product_detail.html', context)


def login(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/login.html', context)


class RegisterView(generics.GenericAPIView):
    serializer_class = AccountRegisterSerializer

    def post(self, request):
        user = request.data
        password = user["password"]
        salt = bcrypt.gensalt()  # Generate a salt for hashing password
        hashed = bcrypt.hashpw(password.encode('utf8'),salt)  # Hash salt with password to save to DB so if someone access to the DB they can't see user's password
        user["salt"] = salt.decode("utf8")
        user["password"] = hashed.decode("utf8")

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        user_data = serializer.data
        del (user_data['salt'])
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    def post(self, request):
        user_email = request.data['email']
        user_password = request.data['password']

        user_obj = Account.objects.filter(id__in=RawSQL('SELECT id FROM home_account WHERE email = %s', [user_email]))
        user_value = user_obj.values()
        username = user_value[0]['username']
        user_id = user_value[0]['id']

        user_salt = user_value[0]['salt']
        encode_salt = bytes(str(user_salt).encode('utf8'))
        hashed = bcrypt.hashpw(user_password.encode('utf8'), encode_salt)
        decode_hashed = hashed.decode('utf8')
        check_hashed = user_value[0]['password']

        now = datetime.now()

        if check_hashed == decode_hashed:
            random_string = get_random_string(length=20)
            byte_jwt = jwt.encode({"some": "payload"}, random_string, algorithm="HS256")
            encoded_jwt = byte_jwt.decode('utf8')
            try:
                Token.objects.get(userID=user_id)
                Token.objects.filter(userID = user_id).update(token=encoded_jwt, created_at=now)
                return Response({
                    'username': username,
                    'userID' : user_id,
                    'email': user_email,
                    'token': encoded_jwt
                }, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                Token.objects.create(userID=user_id, token=encoded_jwt)
                return Response({
                    'username': username,
                    'userID': user_id,
                    'email': user_email,
                    'token': encoded_jwt
                }, status=status.HTTP_200_OK)
        else:
            return Response({
             'error_message': 'Email or password is incorrect!',
             'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

class CheckoutView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self,request):
        user_token = request.data['token']
        check_token = token_check(user_token)
        if check_token is True:
            order = request.data

            serializer = self.serializer_class(data=order)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            order_data = serializer.data
            return Response(order_data, status=status.HTTP_201_CREATED)
        else:
            return  Response(status=status.HTTP_400_BAD_REQUEST)