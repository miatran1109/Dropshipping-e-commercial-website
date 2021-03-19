# from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm, forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


class ProductFromShopee(models.Model):
    product_url = models.TextField(max_length=255)
    title = models.TextField(max_length=255)
    supplier = models.TextField(max_length=255)
    img_urls = ArrayField(models.ImageField(blank=True, upload_to='images/'), blank=True)
    variants = ArrayField(models.TextField(), blank=True)
    variant_type = models.TextField()
    description = models.TextField(max_length=255)
    brand = models.TextField(max_length=255)
    categories = ArrayField(models.TextField(), blank=True)
    price = models.TextField(max_length=255)
    price_not_sale = models.TextField(max_length=255)

    def __str__(self):
        return self.title

    # add category
    def single_cat(self):
        obj = self.objects.values_list('categories')  # all categories
        for cat_list in obj:  # (['Shopee', 'Thời Trang Nam', 'Áo thun', 'Áo ngắn tay không cổ'],)
            for cat in cat_list:  # ['Shopee', 'Thời Trang Nam', 'Áo thun', 'Áo ngắn tay không cổ']
                for i in range(1, len(cat)):  # 'Thời Trang Nam'
                    c1 = Category()
                    c1.title = cat[i]
                    c1.slug = cat[i]
                    c1.description = cat[i]
                    # first category is not parent
                    if i == 1:
                        c1.parent = None
                    # the next one is child of previous
                    else:
                        c1.parent_id = Category.objects.get(title=cat[i - 1]).id
                    # if not already in, save
                    if not Category.objects.filter(slug=cat[i]).exists():
                        c1.save()


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Product(models.Model):
    # VARIANTS = (
    #     ('None', 'None'),
    #     ('Size', 'Size'),
    #     ('Color', 'Color'),
    #     ('Size-Color', 'Size-Color'),
    # )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # many to one relation with Category
    title = models.TextField(max_length=255)
    description = models.TextField()
    src_url = models.URLField()
    image = models.ImageField(upload_to='images/', null=False, max_length=500)
    img_url = models.URLField()
    price = models.TextField()
    amount = models.IntegerField(default=0)
    minamount = models.IntegerField(default=3)
    variant = models.TextField(default='None')
    slug = models.SlugField(max_length=500, null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def average_review(self):
        reviews = Comment.objects.filter(product=self).aggregate(average=Avg('rate'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def get_remote_image(self):
        if self.img_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.img_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}", File(img_temp))
        self.save()


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/',  max_length=500)
    img_url = models.URLField()

    def __str__(self):
        return self.title

    def get_remote_image(self):
        if self.img_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.img_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}", File(img_temp))
        self.save()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = {'subject', 'comment', 'rate'}


# class Color(models.Model):
#     name = models.CharField(max_length=20)
#     code = models.CharField(max_length=10, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     def color_tag(self):
#         if self.code is not None:
#             return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
#         else:
#             return ""
#
#
# class Size(models.Model):
#     name = models.CharField(max_length=20)
#     code = models.CharField(max_length=10, blank=True, null=True)
#
#     def __str__(self):
#         return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    # size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    # image_id = models.IntegerField(blank=True, null=True, default=0)
    # quantity = models.IntegerField(default=1)
    # price = models.FloatField()

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage


class Slider(models.Model):
    title = models.CharField(blank=True, max_length=50)
    subtitle = models.CharField(blank=True, max_length=50)
    img = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title
