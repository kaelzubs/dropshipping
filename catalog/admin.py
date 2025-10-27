from django.contrib import admin
from .models import Product, Category, ProductImage

class ProductImageInline(admin.TabularInline):  # or admin.StackedInline
    model = ProductImage
    extra = 1   # how many empty forms to display by default


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'supplier_cost', 'inventory', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'supplier_sku')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}