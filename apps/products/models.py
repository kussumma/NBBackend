from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(upload_to='categories/', default='categories/no_picture.png')
    icon = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    def __str__(self):
        return self.slug
    
class Subcategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(upload_to='subcategories/', default='subcategories/no_picture.png')
    icon = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args,**kwargs)

    def __str__(self):
        return self.slug
    
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args,**kwargs)

    def __str__(self):
        return self.slug
    
class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(upload_to='brands/', default='brands/no_picture.png')
    icon = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args,**kwargs)

    def __str__(self):
        return self.slug

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    discount = models.IntegerField(default=0)
    description = models.TextField()
    brand = models.ForeignKey(Brand, related_name='product_brands', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product_categories', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='product_subcategories', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='product_tags')
    cover = models.ImageField(upload_to='products/', default='products/no_picture.png')
    link = models.URLField(null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args,**kwargs)

    def __str__(self):
        return self.slug

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='user_ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_ratings',on_delete=models.CASCADE)
    star = models.IntegerField(default=0)
    review = models.TextField()
    image = models.ImageField(upload_to='ratings/', default='ratings/no_picture.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.user.email} - {self.star}"

class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='user_wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_wishlist', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.user.email}"

class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='product_stock', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='stock/', default='stock/no_picture.png')
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    other = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.slug} - {self.price}"
