from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    WEIGHT_UNIT_CHOICES = [
        ('kg', 'Kg'),
        ('g', 'Grams'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    short_description = models.CharField(max_length=250, help_text="Shown on product cards / listing page")
    description = models.TextField(help_text="Full description shown on product detail page")
    ingredients = models.TextField(blank=True)
    nutritional_info = models.TextField(blank=True, help_text="e.g. Energy, Protein, Carbs per 100g")

    image = models.ImageField(upload_to='products/main/')

    sku = models.CharField(max_length=50, unique=True)
    weight_value = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNIT_CHOICES, default='kg')

    mrp = models.DecimalField(max_digits=8, decimal_places=2, help_text="Maximum Retail Price (Rs)")
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Actual selling price (Rs)")

    stock = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide from the website without deleting")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def discount_percent(self):
        if self.mrp and self.mrp > 0:
            return round((1 - (self.selling_price / self.mrp)) * 100)
        return 0

    @property
    def weight_display(self):
        return f"{self.weight_value} {self.get_weight_unit_display()}"


class ProductImage(models.Model):
    """Extra gallery images for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"
