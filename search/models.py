# from django.db import models
#
# class Product(models.Model):
#     name=models.CharField(max_length=225)
#     slug=models.SlugField(max_length=225, unique=True)
#     subcategory=models.ForeignKey('SubCategory', related_name='prosubcat', on_delete=models.CASCADE, blank=True, null=True)
#     totalprice=models.IntegerField()
#     saleprice = models.IntegerField()
#     discount = models.IntegerField(default=None)
#     title=models.CharField(max_length=225)
#     description = models.TextField()
#     overview = models.TextField(null=True)
#     featured = models.BooleanField(null=True)
#     image= models.ImageField(blank=True)
#     # tags = TaggableManager()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)