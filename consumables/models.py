from django.db import models
import uuid


class Consumable(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.CharField(max_length=255)
    expiration = models.DateField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=255)
    stock = models.ForeignKey(
        'stock.Stock', related_name='consumables', on_delete=models.CASCADE)
