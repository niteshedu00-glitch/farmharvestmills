from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).select_related('category')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
        'active_category': active_category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, 'products/detail.html', {
        'product': product,
        'related_products': related_products,
    })
