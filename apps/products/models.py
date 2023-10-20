from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from tools.filestorage_helper import GridFSStorage
from tools.profanity_helper import AdvancedProfanityFilter

User = get_user_model()


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(
        storage=GridFSStorage(collection="categories"), default="default.jpg"
    )
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Subcategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(
        storage=GridFSStorage(collection="subcategories"), default="default.jpg"
    )
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Subsubcategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(
        storage=GridFSStorage(collection="subsubcategories"), default="default.jpg"
    )
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    subcategory = models.ForeignKey(
        Subcategory, related_name="subsubcategories", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subsubcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    origin = models.CharField(max_length=250, null=True, blank=True)
    cover = models.ImageField(
        storage=GridFSStorage(collection="brands"), default="default.jpg"
    )
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    discount = models.IntegerField(default=0)
    description = models.TextField()
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
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name="user_ratings", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_ratings", on_delete=models.CASCADE
    )
    star = models.IntegerField(default=0)
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
        profanity_filter = AdvancedProfanityFilter("words_blacklist.txt", "words_whitelist.txt")
        self.review = profanity_filter.censor(self.review)
        super(Rating, self).save(*args, **kwargs)


class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, related_name="product_stock", on_delete=models.CASCADE
    )
    price = models.IntegerField(default=0)
    image = models.ImageField(
        storage=GridFSStorage(collection="stock_images"), default="default.jpg"
    )
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    other = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.price}"


class ExtraProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, related_name="product_extra_images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        storage=GridFSStorage(collection="extra_product_images"), default="default.jpg"
    )

    def __str__(self):
        return f"{self.product.slug} - {self.image}"
