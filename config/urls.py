from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views as core_views

urlpatterns = [
    path('admin/dashboard/', core_views.admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),

    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('our-process/', core_views.process, name='process'),
    path('quality/', core_views.quality, name='quality'),
    path('farmers/', core_views.farmers, name='farmers'),
    path('privacy-policy/', core_views.privacy_policy, name='privacy_policy'),
    path('terms/', core_views.terms, name='terms'),

    path('products/', include('apps.products.urls')),
    path('blog/', include('apps.blog.urls')),
    path('', include('apps.enquiries.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Farm Harvest Mills — Admin"
admin.site.site_title = "Farm Harvest Mills Admin"
admin.site.index_title = "Dashboard"
