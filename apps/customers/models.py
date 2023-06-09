from django.db import models
from django.contrib.auth import get_user_model
import uuid

from apps.products.models import Product

User = get_user_model()

REQUEST_STATUS = (
    ('pending', 'Pending'),
    ('unrelated', 'Unrelated'),
    ('duplicate', 'Duplicate'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected')
)

BUG_STATUS = (
    ('pending', 'Pending'),
    ('unrelated', 'Unrelated'),
    ('duplicate', 'Duplicate'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
    ('rejected', 'Rejected')
)

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favorites', editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.product.slug}'
    
class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_complaints', editable=False)
    content = models.TextField()
    sugestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.product.slug}'
    
class ComplaintImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='complaint_images')
    image = models.ImageField(upload_to='complaints/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.complaint.user.email} - {self.complaint.product.slug}'
    
class ProductRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requests', editable=False)
    image = models.ImageField(upload_to='requests/')
    title = models.CharField(max_length=255)
    detail = models.TextField()
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.title}'
    
class FeatureRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_features', editable=False)
    title = models.CharField(max_length=255)
    detail = models.TextField()
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.product.slug}'
    
class BugReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reports', editable=False)
    title = models.CharField(max_length=255)
    detail = models.TextField()
    how_to_reproduce = models.TextField()
    result_expected = models.TextField()
    suggestion = models.TextField()
    status = models.CharField(max_length=255, choices=BUG_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.product.slug}'
    
class BugReportImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bug_report = models.ForeignKey(BugReport, on_delete=models.CASCADE, related_name='bug_report_images')
    image = models.ImageField(upload_to='bug_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bug_report.title} - {self.bug_report.created_at}'
