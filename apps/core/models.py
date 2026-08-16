from django.db import models


class Banner(models.Model):
    """Homepage hero / promotional banners, fully editable from admin."""
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True, default='Explore Our Products')
    button_link = models.CharField(max_length=200, blank=True, default='/products/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_role = models.CharField(max_length=100, blank=True, help_text="e.g. Home Chef, Retailer, Distributor")
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"


class SiteSettings(models.Model):
    """
    Singleton-style model so non-technical staff can edit small bits of
    homepage copy without touching code. Only one row is expected to exist.
    """
    hero_heading = models.CharField(max_length=150, default="Pure Grains. Trusted Quality.")
    hero_subheading = models.TextField(
        default="At Farm Harvest Mills, we believe that good food begins with good grains. "
                "We carefully source quality grains and process them with care to deliver fresh, "
                "wholesome and reliable food products for every Indian family."
    )
    about_snippet = models.TextField(
        default="Farm Harvest Mills was built with a simple belief: quality food starts with quality grains."
    )
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    google_maps_embed = models.TextField(blank=True, help_text="Paste the Google Maps embed <iframe> code")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
