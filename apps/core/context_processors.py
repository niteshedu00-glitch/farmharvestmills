from django.conf import settings
from .models import SiteSettings


def site_info(request):
    from apps.products.models import Category
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
        'CONTACT_PHONE': settings.CONTACT_PHONE,
        'CONTACT_ADDRESS': settings.CONTACT_ADDRESS,
        'site_settings': SiteSettings.load(),
        'categories_footer': Category.objects.all()[:7],
    }
