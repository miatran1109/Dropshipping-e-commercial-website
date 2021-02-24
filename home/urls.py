from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views
from .views import UserLoginView, RegisterView

urlpatterns = [
    # Leave as empty string for base url
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('account/', views.account, name="account"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('aboutus/', views.about_us, name="about_us"),
    path('contactus/', views.contact_us, name="contact"),
    path('service/', views.service, name="service"),
    path('faq/', views.faq, name="faq"),
    path('policy/', views.policy, name="policy"),
    path('shop/', views.product_list, name="product_list"),
    path('product/<int:id>/<slug:slug>', views.product_detail, name="product_detail"),
    path('login/', views.login, name="login"),
    path('api/register/', RegisterView.as_view(), name="register"),
    path('api/authenticate', UserLoginView.as_view(), name="authenticate")
    # path('category/<int:id>/<slug:slug>', views.category_product, name="cat_pro"),
]
