from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import mail_admins
from .forms import EnquiryForm, NewsletterForm


def contact_view(request):
    initial = {}
    if request.GET.get('type'):
        initial['enquiry_type'] = request.GET.get('type')

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            if settings.ADMIN_NOTIFY_EMAIL:
                try:
                    mail_admins(
                        subject=f"New Enquiry: {enquiry.name} ({enquiry.get_enquiry_type_display()})",
                        message=f"{enquiry.message}\n\nPhone: {enquiry.phone}\nEmail: {enquiry.email}",
                        fail_silently=True,
                    )
                except Exception:
                    pass
            messages.success(request, "Thank you! Your enquiry has been received. Our team will contact you shortly.")
            return redirect('enquiries:contact')
    else:
        form = EnquiryForm(initial=initial)

    return render(request, 'enquiries/contact.html', {'form': form})


def wholesale_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.enquiry_type = 'wholesale'
            enquiry.save()
            messages.success(request, "Thank you! Your business enquiry has been received. Our team will get in touch soon.")
            return redirect('enquiries:wholesale')
    else:
        form = EnquiryForm(initial={'enquiry_type': 'wholesale'})

    return render(request, 'enquiries/wholesale.html', {'form': form})


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You're subscribed! Thanks for joining Farm Harvest Mills.")
        else:
            messages.error(request, "Please enter a valid email address.")
    return redirect(request.POST.get('next', '/'))
