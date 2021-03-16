from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Cart, CartItem

##-------------- Cart Views --------------------------------------
class DetailCart(DetailView):
    model = Cart
    template_name='cart/detail_cart.html'

class ListCart(ListView):
    model = Cart
    context_object_name = 'carts'
    template_name='cart/list_carts.html'

class CreateCart(CreateView):
    model = Cart
    template_name = 'cart/create_cart.html'

class Updatecart(UpdateView):
    model = Cart
    template_name = 'cart/update_cart.html'

class DeleteCart(DeleteView):
    model = Cart
    template_name = 'cart/delete_cart.html'


##-------------- CartItem Views --------------------------------------
class DetailCartItem(DetailView):
    model = CartItem
    template_name='cartitem/detail_cartitem.html'

class ListCartItem(ListView):
    model = CartItem
    context_object_name = 'cartitems'
    template_name='cartitem/list_cartitems.html'

class CreateItemCart(CreateView):
    model = CartItem
    template_name = 'cartitem/create_cartitem.html'

class UpdateCartItem(UpdateView):
    model = CartItem
    template_name = 'cartitem/update_cartitem.html'

class DeleteCartItem(DeleteView):
    model = Cart
    template_name = 'cartitem/delete_cartitem.html'