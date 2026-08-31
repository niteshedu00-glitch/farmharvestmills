"""
Email notifications for enquiry form submissions.

Two emails are sent when someone submits the contact/wholesale form:
1. To the business (ADMIN_NOTIFY_EMAIL) — so staff see the enquiry immediately.
2. To the customer — a short confirmation so they know it was received.

Both are best-effort: if email sending fails (e.g. SMTP not configured yet),
the enquiry is still saved to the database and visible in /admin/ regardless.
"""
import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_new_enquiry(enquiry):
    if not settings.ADMIN_NOTIFY_EMAIL:
        return  # Not configured yet — enquiry is still saved and visible in admin.

    subject = f"New {enquiry.get_enquiry_type_display()} — {enquiry.name}"
    body = (
        f"A new enquiry was submitted on the {settings.SITE_NAME} website.\n\n"
        f"Type: {enquiry.get_enquiry_type_display()}\n"
        f"Name: {enquiry.name}\n"
        f"Phone: {enquiry.phone}\n"
        f"Email: {enquiry.email}\n"
        f"Company: {enquiry.company_name or '-'}\n\n"
        f"Message:\n{enquiry.message}\n\n"
        f"---\n"
        f"View and manage this enquiry in the admin panel."
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_NOTIFY_EMAIL],
            fail_silently=False,
        )
    except Exception:
        # Never let an email failure break the customer's form submission.
        logger.exception("Failed to send enquiry notification email for enquiry id=%s", enquiry.pk)


def send_customer_confirmation(enquiry):
    subject = f"We received your enquiry — {settings.SITE_NAME}"
    body = (
        f"Hi {enquiry.name},\n\n"
        f"Thank you for reaching out to {settings.SITE_NAME}. We've received your enquiry "
        f"and our team will get back to you shortly at {enquiry.phone} or this email address.\n\n"
        f"Your message:\n\"{enquiry.message}\"\n\n"
        f"— {settings.SITE_NAME} Team\n"
        f"{settings.CONTACT_PHONE} | {settings.CONTACT_EMAIL}"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[enquiry.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send customer confirmation email for enquiry id=%s", enquiry.pk)