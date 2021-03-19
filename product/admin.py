import decimal

from django.contrib import admin
from django.utils.text import slugify
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
    ordering = ['title']
    search_fields = ['title']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]

    # def apply_discount(self, request, queryset):
    #     for prod in queryset:
    #         prod.price = decimal.Decimal(prod.price) * decimal.Decimal('0.9')
    #         prod.save()
    #
    # actions = [apply_discount]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'create_at']
    readonly_fields = ('subject', 'comment', 'ip', 'product', 'rate', 'id')


# class ColorAdmin(admin.ModelAdmin):
#     list_display = ['name', 'code', 'color_tag']
#
#
# class SizeAdmin(admin.ModelAdmin):
#     list_display = ['name', 'code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product']  # , 'color', 'size', 'price', 'quantity'


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'img']


class ShopeeAdmin(admin.ModelAdmin):
    list_display = ['title', 'variants']
    readonly_fields = ['product_url', 'img_urls',
                       'price', 'description', 'categories',
                       'variants', 'brand', 'supplier']

    def add_to_product(self, request, queryset):
        product = Product()
        for qur in queryset:
            product.title = qur.title
            product.slug = slugify(qur.title)
            product.description = qur.description
            product.price = qur.price
            product.src_url = qur.product_url
            product.variant = qur.variant_type
            # category
            cat_list = qur.categories
            cat_id = Category.objects.get(title=cat_list[len(cat_list) - 1]).id
            product.category_id = cat_id

            # image
            images_list = qur.img_urls
            product.img_url = images_list[0]

            if not Product.objects.filter(slug=qur.title).exists():
                product.image = product.get_remote_image()

            # get images
            images_list = qur.img_urls
            for i in range(1, len(images_list)):
                img = Images()
                img.product = Product.objects.get(title=qur.title)
                img.img_url = images_list[i]
                img.image = img.get_remote_image()

            # get variants
            var_list = qur.variants
            for i in range(len(var_list)):
                var = Variants()
                var.title = var_list[i]
                var.product = Product.objects.get(title=qur.title)
                var.save()

            # delete this product from this model
            # qur.delete()

    actions = [add_to_product]


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductFromShopee, ShopeeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images, ImagesAdmin)
# admin.site.register(Color, ColorAdmin)
# admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Slider, SliderAdmin)
