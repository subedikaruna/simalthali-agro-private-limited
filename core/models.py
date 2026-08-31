from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from urllib.parse import urlparse, parse_qs


def youtube_embed_url(url):
    """
    Turn a normal YouTube link (youtu.be/xxx or youtube.com/watch?v=xxx) into
    an embeddable URL. If it's already an embed link, or from another host
    like Vimeo, it's returned as-is.
    """
    if not url:
        return None
    parsed = urlparse(url)
    if "youtu.be" in parsed.netloc:
        video_id = parsed.path.lstrip("/")
        return f"https://www.youtube.com/embed/{video_id}"
    if "youtube.com" in parsed.netloc:
        if "/embed/" in parsed.path:
            return url
        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
    return url


class HomePage(models.Model):
    """
    Singleton model for the homepage's hero section.
    There will only ever be one row (pk=1) — edit it from the admin panel.

    You can set EITHER a hero image OR a hero video link (not both needed) —
    if a video link is filled in, it takes priority over the image.
    """

    hero_heading = models.CharField(
        max_length=200, default="Raised with care, in the heart of the hills."
    )
    hero_subheading = models.TextField(
        default="Ethically raised goats, fresh milk, and quality breeding stock — straight from our family farm to you."
    )
    hero_image = models.ImageField(
        upload_to="homepage/", blank=True, null=True,
        help_text="Shown as the hero background if no video link is set below.",
    )
    hero_video_url = models.URLField(
        blank=True,
        help_text="Optional. Paste a YouTube link (any format) to show a video instead of the image — it embeds automatically.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

    def __str__(self):
        return "Home Page"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def hero_embed_url(self):
        return youtube_embed_url(self.hero_video_url)


class GalleryItem(models.Model):
    """
    A single photo or video for the homepage's 'From the Farm' gallery.
    Set either an image OR a video link, not both — video takes priority
    if both happen to be filled in.
    """

    caption = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    video_url = models.URLField(
        blank=True, help_text="Optional. A YouTube link — embeds automatically."
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first."
    )
    is_featured = models.BooleanField(default=True, help_text="Show on the homepage.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.caption or f"Gallery item #{self.pk}"

    @property
    def embed_url(self):
        return youtube_embed_url(self.video_url)


class AboutPage(models.Model):
    """
    Singleton model for the About page content.
    There will only ever be one row (pk=1) — edit it from the admin panel
    instead of touching the about.html template directly.
    """

    title = models.CharField(max_length=200, default="About Simalthali Agro Pvt.Ltd.")
    story = models.TextField(
        help_text="Tell your farm's story — how it started, your values, what makes it special."
    )
    photo = models.ImageField(upload_to="about/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Force this to always be the single row with pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent accidental deletion — there should always be exactly one row
        pass

    @classmethod
    def load(cls):
        """Get the About page content, creating a default one if it doesn't exist yet."""
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                "title": "About Simalthali Agro Pvt.Ltd.",
                "story": "Tell your farm's story here — edit this from the admin panel.",
            },
        )
        return obj


class Breed(models.Model):
    """A goat breed you raise on the farm (e.g. Boer, Khari, Jamunapari)."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="breeds/", blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Goat(models.Model):
    """
    Public showcase profile for a goat on your website (e.g. 'Meet our herd').

    NOTE: This is a lightweight, public-facing model. In the next project
    stage (the internal farm web app), we'll add a separate, more detailed
    tracking model (weight history, health records, milk records, etc.)
    that links back to this same goat. Keeping this one simple on purpose.
    """

    SEX_CHOICES = [("M", "Male"), ("F", "Female")]

    name = models.CharField(max_length=100)
    ear_tag_number = models.CharField(
        max_length=30, unique=True, blank=True, null=True,
        help_text="The physical ear tag ID on this goat, e.g. HGF-014. Leave blank if not tagged yet.",
    )
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True, related_name="goats")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    mother = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True,
        limit_choices_to={"sex": "F"}, related_name="offspring_as_mother",
    )
    father = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True,
        limit_choices_to={"sex": "M"}, related_name="offspring_as_father",
    )
    photo = models.ImageField(upload_to="goats/", blank=True, null=True)
    description = models.TextField(blank=True, help_text="A short bio / fun facts about this goat.")
    is_available_for_sale = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False, help_text="Show on the homepage.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("goat_detail", args=[self.pk])


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("milk", "Milk"),
        ("cheese", "Cheese"),
        ("meat", "Meat"),
        ("breeding_stock", "Breeding Stock"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, help_text="e.g. per liter, per kg, per head")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])


class ContactMessage(models.Model):
    """Messages submitted through the public contact form."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"
