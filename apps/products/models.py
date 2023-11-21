from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from colorfield.fields import ColorField
from tools.filestorage_helper import GridFSStorage
from tools.profanity_helper import AdvancedProfanityFilter

User = get_user_model()


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(null=True, blank=True)
    cover = models.ImageField(
        storage=GridFSStorage(collection="categories"),
        default="default.jpg",
        help_text="1220 x 210 px",
    )
    cover_mobile = models.ImageField(
        storage=GridFSStorage(collection="categories_mobile"),
        default="default.jpg",
        help_text="400 x 210 px",
    )
    cover_homepage = models.ImageField(
        storage=GridFSStorage(collection="categories_home"),
        default="default.jpg",
        help_text="220 x 320 px",
    )
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.cover_mobile.delete()
        self.cover_homepage.delete()
        super(Category, self).delete(*args, **kwargs)


class Subcategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(null=True, blank=True)
    cover = models.ImageField(
        storage=GridFSStorage(collection="subcategories"),
        default="default.jpg",
        help_text="1220 x 210 px",
    )
    cover_mobile = models.ImageField(
        storage=GridFSStorage(collection="subcategories_mobile"),
        default="default.jpg",
        help_text="400 x 210 px",
    )
    cover_homepage = models.ImageField(
        storage=GridFSStorage(collection="subcategories_home"),
        default="default.jpg",
        help_text="220 x 320 px",
    )
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.cover_mobile.delete()
        self.cover_homepage.delete()
        super(Subcategory, self).delete(*args, **kwargs)


class Subsubcategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(null=True, blank=True)
    cover = models.ImageField(
        storage=GridFSStorage(collection="subsubcategories"),
        default="default.jpg",
        help_text="1220 x 210 px",
    )
    cover_mobile = models.ImageField(
        storage=GridFSStorage(collection="subsubcategories_mobile"),
        default="default.jpg",
        help_text="400 x 210 px",
    )
    cover_homepage = models.ImageField(
        storage=GridFSStorage(collection="subsubcategories_home"),
        default="default.jpg",
        help_text="220 x 320 px",
    )
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )
    subcategory = models.ForeignKey(
        Subcategory, related_name="subsubcategories", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subsubcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.cover_mobile.delete()
        self.cover_homepage.delete()
        super(Subsubcategory, self).delete(*args, **kwargs)


class Brand(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(null=True, blank=True)
    origin = models.CharField(max_length=250, null=True, blank=True)
    logo = models.ImageField(
        storage=GridFSStorage(collection="brand_logos"),
        default="default.jpg",
        db_index=True,
        help_text="200 x 200 px",
    )
    cover = models.ImageField(
        storage=GridFSStorage(collection="brands"),
        default="default.jpg",
        help_text="1220 x 210 px",
    )
    cover_mobile = models.ImageField(
        storage=GridFSStorage(collection="brands_mobile"),
        default="default.jpg",
        help_text="400 x 210 px",
    )
    cover_homepage = models.ImageField(
        storage=GridFSStorage(collection="brands_home"),
        default="default.jpg",
        help_text="220 x 320 px",
    )
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def delete(self, *args, **kwargs):
        self.logo.delete()
        self.cover.delete()
        self.cover_mobile.delete()
        self.cover_homepage.delete()
        super(Brand, self).delete(*args, **kwargs)


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(null=True, blank=True)
    usage = models.TextField(null=True, blank=True)
    usage_id = models.TextField(null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    ingredients_id = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(
        Brand, related_name="product_brands", on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        Category, related_name="product_categories", on_delete=models.PROTECT
    )
    subcategory = models.ForeignKey(
        Subcategory, related_name="product_subcategories", on_delete=models.PROTECT
    )
    subsubcategory = models.ForeignKey(
        Subsubcategory,
        related_name="product_subsubcategories",
        on_delete=models.PROTECT,
    )
    cover = models.ImageField(
        storage=GridFSStorage(collection="products"),
        default="default.jpg",
        help_text="300 x 300 px",
    )
    link = models.URLField(null=True, blank=True)
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def delete(self, *args, **kwargs):
        self.cover.delete()
        super(Product, self).delete(*args, **kwargs)


class Rating(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, related_name="user_ratings", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_ratings", on_delete=models.CASCADE
    )
    star = models.IntegerField(default=0, db_index=True)
    review = models.TextField()
    image = models.ImageField(
        storage=GridFSStorage(collection="rating_images"),
        default="default.jpg",
    )
    video = models.FileField(
        storage=GridFSStorage(collection="rating_videos"), null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.user.pk} - {self.star}"

    def save(self, *args, **kwargs):
        profanity_filter = AdvancedProfanityFilter()
        self.review = profanity_filter.censor(self.review)
        super(Rating, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.video.delete()
        super(Rating, self).delete(*args, **kwargs)


class Wishlist(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, related_name="user_wishlist", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_wishlist", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.user.pk}"


class Stock(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    product = models.ForeignKey(
        Product, related_name="product_stock", on_delete=models.CASCADE
    )
    sku = models.CharField(max_length=250, unique=True, db_index=True)
    price = models.IntegerField(default=0, db_index=True)
    discount = models.IntegerField(default=0, db_index=True)
    size = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    color = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    color_code = ColorField(null=True, blank=True)
    variant = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    variant_image = models.ImageField(
        storage=GridFSStorage(collection="variant_images"),
        default="default.jpg",
        db_index=True,
        help_text="300 x 300 px",
    )
    quantity = models.IntegerField(default=0, db_index=True)
    weight = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.price}"

    def delete(self, *args, **kwargs):
        self.variant_image.delete()
        super(Stock, self).delete(*args, **kwargs)


class ExtraProductImage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    product = models.ForeignKey(
        Product, related_name="product_extra_images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        storage=GridFSStorage(collection="extra_product_images"),
        default="default.jpg",
        db_index=True,
        help_text="300 x 300 px",
    )

    def __str__(self):
        return f"{self.product.slug} - {self.image}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(ExtraProductImage, self).delete(*args, **kwargs)
