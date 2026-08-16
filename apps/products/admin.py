from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order', 'name')

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumb', 'name', 'category', 'sku', 'weight_display',
        'selling_price', 'mrp', 'stock_badge', 'is_featured', 'is_active',
    )
    list_display_links = ('thumb', 'name')
    list_editable = ('is_featured', 'is_active')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_per_page = 25

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'sku', 'image')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'description', 'ingredients', 'nutritional_info')
        }),
        ('Pricing & Weight', {
            'fields': (('weight_value', 'weight_unit'), ('mrp', 'selling_price'), 'stock')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active')
        }),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return "-"
    thumb.short_description = 'Image'

    def stock_badge(self, obj):
        color = '#16a34a' if obj.stock > 20 else ('#f59e0b' if obj.stock > 0 else '#dc2626')
        return format_html('<b style="color:{}">{}</b>', color, obj.stock)
    stock_badge.short_description = 'Stock'
