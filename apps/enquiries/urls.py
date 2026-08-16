from django.urls import path
from . import views

app_name = 'enquiries'

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('wholesale/', views.wholesale_view, name='wholesale'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
