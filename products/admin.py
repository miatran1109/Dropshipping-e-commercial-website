from django.contrib import admin

# Register your models here.
from products.models import Categories, Product, Images


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Categories, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'description', 'amount']
    list_filter = ['category']


admin.site.register(Product, ProductAdmin)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'title']


admin.site.register(Images, ImagesAdmin)
