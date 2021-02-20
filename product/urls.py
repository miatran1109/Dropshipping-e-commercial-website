from django.urls import path

from . import views


urlpatterns = [
    # Leave as empty string for base url
    path('', views.index, name='index'),
    # path('comment/<int:p_id>', views.product_detail, name='add_comment'),

]
