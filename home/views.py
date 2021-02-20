from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from product.models import *
from .serializers import AccountLoginSerializer, AccountSerializer


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
    comments = Comment.objects.filter(product_id=id, parent=None).order_by('-id')
    context = {'product': product, 'category': category,
               'images': images, 'comments': comments,
               }
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, slug=slug)
    comments = product.comments.filter(parent__isnull=True)
    prod = Product.objects.get(id=id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_id = None

            new_comment = comment_form.save(commit=False)
            new_comment.product_id = id
            user_name = request.settings.AUTH_USER_MODEL
            new_comment.users_id = user_name.id
            try:
                parent_id = request.POST['parent_id']
            except:
                pass
            if parent_id:
                new_comment = comment_form.save(commit=False)
                new_comment.prod = prod
                new_comment.parent = comments.get(id=parent_id)
                new_comment.save()

            new_comment.save()

            return HttpResponseRedirect(url)

    return render(request, 'pages/product_detail.html', context)


def login(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'pages/login.html', context)


def category_product(request, id, slug):
    category = Category.objects.all()
    product_cat = Product.objects.filter(category_id=id)
    paginator = Paginator(product_cat, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {'cat': product_cat, 'category': category, 'page_obj': page_obj}
    return render(request, 'pages/category.html', context)


class Register(generics.GenericAPIView):
    serializer_class = AccountSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)