from django.db import models
import uuid


class Analysis(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    batch = models.CharField(unique=True, max_length=255)
    made = models.DateTimeField(auto_now_add=True)
    class_id = models.CharField(null=True, max_length=255)
    class_data = models.JSONField(null=True)
    category = models.CharField(max_length=255)
    is_concluded = models.BooleanField(default=False)
    analyst = models.ForeignKey(
        'users.User', related_name='analysis', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    consumed_items = models.JSONField(null=True)
