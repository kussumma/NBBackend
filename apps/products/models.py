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
    description_id = models.TextField(
        null=True, blank=True
    )  # ID translation for description
    cover = models.ImageField(
        storage=GridFSStorage(collection="categories"), default="default.jpg"
    )
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Subcategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(
        null=True, blank=True
    )  # ID translation for description
    cover = models.ImageField(
        storage=GridFSStorage(collection="subcategories"), default="default.jpg"
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


class Subsubcategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(
        null=True, blank=True
    )  # ID translation for description
    cover = models.ImageField(
        storage=GridFSStorage(collection="subsubcategories"), default="default.jpg"
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


class Brand(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(
        null=True, blank=True
    )  # ID translation for description
    origin = models.CharField(max_length=250, null=True, blank=True)
    logo = models.ImageField(
        storage=GridFSStorage(collection="brand_logos"),
        default="default.jpg",
        db_index=True,
    )
    cover = models.ImageField(
        storage=GridFSStorage(collection="brands"), default="default.jpg"
    )
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(null=True, blank=True)
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
        storage=GridFSStorage(collection="products"), default="default.jpg"
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
        storage=GridFSStorage(collection="rating_videos"),
        default="default.jpg",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.user.pk} - {self.star}"

    def save(self, *args, **kwargs):
        profanity_filter = AdvancedProfanityFilter()
        self.review = profanity_filter.censor(self.review)
        super(Rating, self).save(*args, **kwargs)


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
    image = models.ImageField(
        storage=GridFSStorage(collection="stock_images"), default="default.jpg"
    )
    size = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    color = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    color_code = ColorField(null=True, blank=True)
    other = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0, db_index=True)
    weight = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.price}"


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
    )

    def __str__(self):
        return f"{self.product.slug} - {self.image}"
