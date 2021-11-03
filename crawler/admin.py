from django.contrib import admin
from .models import Product, Feature, Images as Image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'deal_price', 'seller', 'code', 'stars', 'count']
    sortable_by = ['id']  # the products are sorted by the order of id
    list_filter = ['brand', 'seller']  # we can filter products based on brand and seller
    search_fields = ['title']  # we can search between products by there name


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['product', 'content']
    list_filter = ['product']  # we can filter features based on product


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'content']
    list_filter = ['product']
