from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.products.models import Product, Category
from apps.enquiries.models import Enquiry
from apps.blog.models import BlogPost
from .models import Banner, Testimonial


def home(request):
    context = {
        'banners': Banner.objects.filter(is_active=True),
        'featured_products': Product.objects.filter(is_active=True, is_featured=True)[:8],
        'categories': Category.objects.all()[:8],
        'testimonials': Testimonial.objects.filter(is_active=True),
        'recent_posts': BlogPost.objects.filter(is_published=True)[:3],
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def process(request):
    return render(request, 'core/process.html')


def quality(request):
    return render(request, 'core/quality.html')


def farmers(request):
    return render(request, 'core/farmers.html')


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def terms(request):
    return render(request, 'core/terms.html')


@staff_member_required
def admin_dashboard(request):
    """Custom dashboard shown at /admin/dashboard/, styled to match Django admin."""
    context = dict(
        title="Dashboard",
        product_count=Product.objects.count(),
        category_count=Category.objects.count(),
        low_stock_products=Product.objects.filter(stock__lt=10, is_active=True).order_by('stock')[:6],
        low_stock_count=Product.objects.filter(stock__lt=10, is_active=True).count(),
        enquiry_count=Enquiry.objects.count(),
        new_enquiry_count=Enquiry.objects.filter(status='new').count(),
        recent_enquiries=Enquiry.objects.all()[:6],
        blog_count=BlogPost.objects.filter(is_published=True).count(),
        has_permission=True,
    )
    return render(request, 'admin/dashboard.html', context)
