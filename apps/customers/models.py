from django.db import models
from django.contrib.auth import get_user_model
import uuid
from tools.filestorage_helper import GridFSStorage
from tools.profanity_helper import AdvancedProfanityFilter

from apps.products.models import Product

User = get_user_model()

REQUEST_STATUS = (
    ("pending", "Pending"),
    ("unrelated", "Unrelated"),
    ("duplicate", "Duplicate"),
    ("accepted", "Accepted"),
    ("rejected", "Rejected"),
)

BUG_STATUS = (
    ("pending", "Pending"),
    ("unrelated", "Unrelated"),
    ("duplicate", "Duplicate"),
    ("in_progress", "In Progress"),
    ("resolved", "Resolved"),
    ("rejected", "Rejected"),
)


class Favorite(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_favorites"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_favorites"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.slug}"


class Complaint(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_complaints"
    )
    content = models.TextField()
    sugestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.id}"

    def save(self, *args, **kwargs):
        self.content = AdvancedProfanityFilter().censor(self.content)
        self.sugestion = AdvancedProfanityFilter().censor(self.sugestion)
        super(Complaint, self).save(*args, **kwargs)


class ComplaintImage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="complaint_images"
    )
    image = models.ImageField(
        storage=GridFSStorage(collection="complaint_images"), default="default.jpg"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(ComplaintImage, self).delete(*args, **kwargs)


class ProductRequest(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_requests"
    )
    image = models.ImageField(
        storage=GridFSStorage(collection="product_request_images"),
        default="default.jpg",
    )
    title = models.CharField(max_length=255)
    detail = models.TextField()
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    def save(self, *args, **kwargs):
        self.detail = AdvancedProfanityFilter().censor(self.detail)
        super(ProductRequest, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(ProductRequest, self).delete(*args, **kwargs)


class FeatureRequest(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_features"
    )
    title = models.CharField(max_length=255)
    detail = models.TextField()
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    def save(self, *args, **kwargs):
        self.detail = AdvancedProfanityFilter().censor(self.detail)
        super(FeatureRequest, self).save(*args, **kwargs)


class BugReport(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reports"
    )
    title = models.CharField(max_length=255)
    detail = models.TextField()
    how_to_reproduce = models.TextField()
    result_expected = models.TextField()
    suggestion = models.TextField()
    status = models.CharField(max_length=255, choices=BUG_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    def save(self, *args, **kwargs):
        self.detail = AdvancedProfanityFilter().censor(self.detail)
        self.how_to_reproduce = AdvancedProfanityFilter().censor(self.how_to_reproduce)
        self.result_expected = AdvancedProfanityFilter().censor(self.result_expected)
        self.suggestion = AdvancedProfanityFilter().censor(self.suggestion)
        super(BugReport, self).save(*args, **kwargs)


class BugReportImage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    bug_report = models.ForeignKey(
        BugReport, on_delete=models.CASCADE, related_name="bug_report_images"
    )
    image = models.ImageField(
        storage=GridFSStorage(collection="bug_report_images"), default="default.jpg"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(BugReportImage, self).delete(*args, **kwargs)
