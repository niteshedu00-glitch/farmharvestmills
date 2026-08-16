import io
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from apps.products.models import Category, Product
from apps.blog.models import BlogPost
from apps.core.models import Testimonial, Banner


def make_placeholder(text, size=(800, 800), bg=(214, 168, 96), fg=(255, 255, 255)):
    img = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=fg, font=font)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85)
    return ContentFile(buf.getvalue(), name=f"{text.lower().replace(' ', '_')}.jpg")


class Command(BaseCommand):
    help = "Seed the database with sample categories, products, a blog post and testimonials."

    def handle(self, *args, **options):
        cat_data = [
            ("Atta", "Whole wheat and specialty flours for everyday rotis."),
            ("Refined Flour", "Fine milled flour for a range of recipes."),
            ("Grains & Dalia", "Wholesome grain products for nutritious meals."),
        ]
        categories = {}
        for i, (name, desc) in enumerate(cat_data):
            cat, _ = Category.objects.get_or_create(name=name, defaults={'description': desc, 'order': i})
            categories[name] = cat
        self.stdout.write(self.style.SUCCESS(f"Categories: {len(categories)}"))

        products_data = [
            ("Whole Wheat Atta", "Atta", "Freshly milled whole wheat flour for soft, wholesome rotis.",
             "Made from 100% whole wheat grains, stone-ground for a fine, consistent texture ideal for everyday Indian meals.",
             "Whole Wheat", "Energy 340 kcal, Protein 12g, Carbs 71g per 100g", "WA-5KG", 5, 'kg', 260, 220, 45, True),
            ("Sharbati Atta", "Atta", "Rich taste and smooth texture from select Sharbati wheat.",
             "Sourced from Sharbati wheat known for its naturally sweet flavor and soft, fluffy rotis.",
             "Sharbati Wheat", "Energy 345 kcal, Protein 12g, Carbs 72g per 100g", "SA-5KG", 5, 'kg', 320, 280, 30, True),
            ("Multigrain Atta", "Atta", "A nutritious blend of selected grains for everyday variety.",
             "A wholesome mix of wheat, jowar, bajra, ragi and chana for added fibre and nutrition.",
             "Wheat, Jowar, Bajra, Ragi, Chana", "Energy 350 kcal, Protein 13g, Fibre 9g per 100g", "MA-5KG", 5, 'kg', 300, 260, 8, True),
            ("Maida (Refined Flour)", "Refined Flour", "Fine wheat flour for traditional and modern recipes.",
             "Finely milled refined flour suitable for breads, pastries, and a wide range of recipes.",
             "Refined Wheat Flour", "Energy 348 kcal, Protein 10g, Carbs 76g per 100g", "MD-1KG", 1, 'kg', 60, 52, 60, False),
            ("Sooji (Semolina)", "Refined Flour", "Carefully processed semolina for breakfast and sweets.",
             "Coarse-milled wheat semolina, perfect for upma, halwa and a range of classic dishes.",
             "Wheat Semolina", "Energy 360 kcal, Protein 12g, Carbs 73g per 100g", "SJ-1KG", 1, 'kg', 65, 55, 3, False),
            ("Besan (Gram Flour)", "Refined Flour", "Quality gram flour for pakoras, chilla and sweets.",
             "Made from finely milled chana dal, ideal for savoury snacks and traditional sweets.",
             "Chana Dal (Gram)", "Energy 387 kcal, Protein 22g, Carbs 58g per 100g", "BS-1KG", 1, 'kg', 90, 78, 40, False),
            ("Dalia (Broken Wheat)", "Grains & Dalia", "A wholesome grain for a nutritious breakfast.",
             "Coarsely broken wheat, rich in fibre — cooks quickly into a light, nutritious porridge.",
             "Broken Wheat", "Energy 342 kcal, Protein 11g, Fibre 12g per 100g", "DL-1KG", 1, 'kg', 55, 48, 25, False),
        ]

        for name, cat_name, short_desc, desc, ingredients, nutrition, sku, wv, wu, mrp, price, stock, featured in products_data:
            if Product.objects.filter(sku=sku).exists():
                continue
            p = Product(
                name=name, category=categories[cat_name], short_description=short_desc,
                description=desc, ingredients=ingredients, nutritional_info=nutrition,
                sku=sku, weight_value=wv, weight_unit=wu, mrp=mrp, selling_price=price,
                stock=stock, is_featured=featured, is_active=True,
            )
            p.image.save(f"{sku}.jpg", make_placeholder(name.split()[0]), save=False)
            p.save()
        self.stdout.write(self.style.SUCCESS(f"Products: {Product.objects.count()}"))

        if not BlogPost.objects.exists():
            post = BlogPost(
                title="5 Reasons Fresh-Milled Atta Makes Softer Rotis",
                excerpt="Discover why freshly milled whole wheat flour makes a real difference in your daily rotis.",
                content=(
                    "Freshly milled atta retains more of the wheat's natural oils and nutrients compared to "
                    "flour that has sat on a shelf for months. This freshness translates directly into softer, "
                    "more flavourful rotis on your table.\n\n"
                    "At Farm Harvest Mills, we mill in small batches so the atta reaching your kitchen is as "
                    "close to farm-fresh as possible. Here's what makes the difference: consistent grain "
                    "selection, controlled milling temperature, and quick turnaround from mill to package."
                ),
                author="Farm Harvest Mills Team",
            )
            post.thumbnail.save("blog_atta.jpg", make_placeholder("Fresh Atta", size=(1200, 630)), save=False)
            post.save()
        self.stdout.write(self.style.SUCCESS("Blog post created"))

        testimonials = [
            ("Priya Sharma", "Home Chef", "The rotis turn out so soft every single time. We won't switch back!", 5),
            ("Rajesh Traders", "Retailer, Ghaziabad", "Reliable quality and on-time bulk delivery every month.", 5),
            ("Anita Verma", "Home Chef", "You can really taste the difference with fresh atta.", 4),
        ]
        for i, (name, role, quote, rating) in enumerate(testimonials):
            Testimonial.objects.get_or_create(customer_name=name, defaults={
                'customer_role': role, 'quote': quote, 'rating': rating, 'order': i
            })
        self.stdout.write(self.style.SUCCESS("Testimonials created"))

        if not Banner.objects.exists():
            b = Banner(title="Pure Grains. Trusted Quality.",
                       subtitle="From Farm to Family — freshly milled atta, maida, sooji and besan.",
                       button_text="Explore Our Products", button_link="/products/", order=0)
            b.image.save("hero_banner.jpg", make_placeholder("Farm Harvest Mills", size=(1600, 700), bg=(150, 96, 31)), save=False)
            b.save()
        self.stdout.write(self.style.SUCCESS("Banner created"))

        self.stdout.write(self.style.SUCCESS("Seed complete."))
