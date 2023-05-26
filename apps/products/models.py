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
    icon = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(upload_to='subcategories/', default='subcategories/no_picture.png')
    icon = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args,**kwargs)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    color = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args,**kwargs)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(upload_to='brands/', default='brands/no_picture.png')
    icon = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    description = models.TextField()
    brand = models.ForeignKey(Brand, related_name='product_brands', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product_categories', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='product_subcategories', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='product_tags')
    cover = models.ImageField(upload_to='products/', default='products/no_picture.png')
    tutorial = models.URLField(null=True, blank=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args,**kwargs)

    def __str__(self):
        return self.name
    
    def increment_views(self):
        self.views += 1
        self.save()

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='user_ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_ratings',on_delete=models.CASCADE)
    star = models.IntegerField(default=0)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.slug} - {self.user.email} - {self.star}"

class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='product_stock', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stock/', default='stock/no_picture.png')
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    other = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    purchase_price = models.IntegerField(default=0)
    purchase_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.color is None:
            return f"{self.product.slug} - {self.size} - {self.other} -  {self.quantity}"
        elif self.size is None:
            return f"{self.product.slug} - {self.color} - {self.other} - {self.quantity}"
        elif self.other is None:
            return f"{self.product.slug} - {self.size} - {self.color} - {self.quantity}"
        else:
            return f"{self.product.slug} - {self.size} - {self.color} - {self.other} - {self.quantity}"
