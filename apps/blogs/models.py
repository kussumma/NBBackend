from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from tools.filestorage_helper import GridFSStorage
from tools.profanity_helper import AdvancedProfanityFilter

User = get_user_model()


class BlogCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    description_id = models.TextField(null=True, blank=True)
    cover = models.ImageField(
        storage=GridFSStorage(collection="blog_categories"),
        null=True,
        blank=True,
        db_index=True,
        help_text="1220 x 210 px",
    )
    cover_mobile = models.ImageField(
        storage=GridFSStorage(collection="blog_categories_mobile"),
        null=True,
        blank=True,
        db_index=True,
        help_text="400 x 210 px",
    )
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.cover_mobile.delete()
        super(BlogCategory, self).delete(*args, **kwargs)


class BlogTag(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BlogTag, self).save(*args, **kwargs)


class Blog(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    title = models.CharField(max_length=250, unique=True)
    title_id = models.CharField(max_length=250, null=True, blank=True, unique=True)
    content = models.TextField()
    content_id = models.TextField(null=True, blank=True)
    cover = models.ImageField(
        storage=GridFSStorage(collection="blog_covers"),
        null=True,
        blank=True,
        db_index=True,
        help_text="1220 x 210 px",
    )
    cover_mobile = models.ImageField(
        storage=GridFSStorage(collection="blog_covers_mobile"),
        null=True,
        blank=True,
        db_index=True,
        help_text="400 x 210 px",
    )
    cover_homepage = models.ImageField(
        storage=GridFSStorage(collection="blog_covers_home"),
        null=True,
        blank=True,
        db_index=True,
        help_text="600 x 280 px",
    )
    cover_homepage_mobile = models.ImageField(
        storage=GridFSStorage(collection="blog_covers_home_mobile"),
        null=True,
        blank=True,
        db_index=True,
        help_text="400 x 280 px",
    )
    cover_homepage_headline = models.ImageField(
        storage=GridFSStorage(collection="blog_covers_home_headline"),
        null=True,
        blank=True,
        db_index=True,
        help_text="600 x 600 px",
    )
    slug = models.SlugField(
        max_length=250, unique=True, null=True, blank=True, db_index=True
    )
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT)
    tags = models.ManyToManyField(BlogTag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    is_published = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=False)
    is_headline = models.BooleanField(default=False, db_index=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.cover_mobile.delete()
        self.cover_homepage.delete()
        self.cover_homepage_mobile.delete()
        self.cover_homepage_headline.delete()
        super(Blog, self).delete(*args, **kwargs)


class BlogImage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(
        storage=GridFSStorage(collection="blog_images"),
        null=True,
        blank=True,
        db_index=True,
        help_text="600 x 600 px",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(BlogImage, self).delete(*args, **kwargs)


class BlogVideo(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    video = models.URLField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlogUrl(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    url = models.URLField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlogComment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        related_query_name="reply",
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk

    def save(self, *args, **kwargs):
        self.comment = AdvancedProfanityFilter().censor(self.comment)
        super(BlogComment, self).save(*args, **kwargs)
