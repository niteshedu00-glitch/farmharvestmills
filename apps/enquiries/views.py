from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EnquiryForm, NewsletterForm
from .emails import notify_new_enquiry, send_customer_confirmation


def contact_view(request):
    initial = {}
    if request.GET.get('type'):
        initial['enquiry_type'] = request.GET.get('type')

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            notify_new_enquiry(enquiry)
            send_customer_confirmation(enquiry)
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
            notify_new_enquiry(enquiry)
            send_customer_confirmation(enquiry)
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