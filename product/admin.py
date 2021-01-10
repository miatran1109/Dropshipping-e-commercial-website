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

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

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
    list_display = ['title', 'category', 'image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'create_at']
    list_filter = ['status']
    readonly_fields = ('subject', 'comment', 'ip', 'user', 'product', 'rate', 'id')


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'price', 'quantity', 'image_tag']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
