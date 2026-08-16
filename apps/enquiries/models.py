from django.db import models


class Enquiry(models.Model):
    TYPE_CHOICES = [
        ('general', 'General Enquiry'),
        ('retail', 'Retail Customer'),
        ('wholesale', 'Wholesale / Bulk'),
        ('distributor', 'Distributor / Business Partner'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    company_name = models.CharField(max_length=150, blank=True)
    enquiry_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    message = models.TextField()

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True, help_text="Internal notes, not visible to the customer")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.get_enquiry_type_display()} ({self.created_at:%d %b %Y})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
