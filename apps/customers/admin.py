from django.contrib import admin

from .models import (
    Favorite,
    Complaint,
    ComplaintImage,
    ProductRequest,
    FeatureRequest,
    BugReport,
    BugReportImage,
    Subscription,
)

admin.site.register(Favorite)
admin.site.register(Complaint)
admin.site.register(ComplaintImage)
admin.site.register(ProductRequest)
admin.site.register(FeatureRequest)
admin.site.register(BugReport)
admin.site.register(BugReportImage)
admin.site.register(Subscription)
