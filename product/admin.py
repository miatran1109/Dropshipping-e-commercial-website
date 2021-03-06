from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *


# Register your models here.
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'


class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'title']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'create_at']
    readonly_fields = ('subject', 'comment', 'ip', 'product', 'rate', 'id')


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'price', 'quantity', 'image_tag']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'img']


class ShopeeAdmin(admin.ModelAdmin):
    list_display = ['title']
    readonly_fields = ['title', 'product_url', 'img_urls',
                       'price', 'description', 'categories',
                       'variants', 'brand', 'supplier']

    def add_to_product(self, request, queries):
        product = Product
        for qur in queries:
            product = qur.save()

    actions = [add_to_product]


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductFromShopee, ShopeeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Slider, SliderAdmin)
