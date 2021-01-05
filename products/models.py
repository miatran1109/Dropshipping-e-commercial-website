from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from sqlparse.sql import Comment


class Categories(models.Model):
    title = models.CharField(max_length=50)  # title of category
    description = models.TextField(max_length=255)  # description of category
    image = models.ImageField(blank=True, upload_to='images/')  # image of category
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    # to choose type of product
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)  # Foreign key from Category
    title = models.CharField(max_length=150)  # Name of products
    description = models.TextField(max_length=255)  # Description of product
    image = models.ImageField(upload_to='images/', null=False)  # Image of product
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # Price of product
    amount = models.IntegerField(default=0)  # How many are on suppliers' store
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')  # Information of product if choosen
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Foreign key from product
    title = models.CharField(max_length=50, blank=True)  # Name of product that this images show
    image = models.ImageField(blank=True, upload_to='images/')  # Link to the image

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

    def color_title(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            var_image = img.image.url
        else:
            var_image = ""
        return var_image


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'comment', 'rate']


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=225)
    shipper = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
