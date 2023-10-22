from django.db import models
from django.contrib.auth import get_user_model
import uuid
from tools.profanity_helper import AdvancedProfanityFilter

User = get_user_model()


class Search(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.CharField(max_length=250)
    user = models.ForeignKey(
        User, related_name="searches", on_delete=models.PROTECT, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

    def save(self, *args, **kwargs):
        self.query = AdvancedProfanityFilter().censor(self.query)
        super(Search, self).save(*args, **kwargs)
