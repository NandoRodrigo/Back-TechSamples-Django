from django.db import models
import uuid
from consumables.models import Consumable


class Stock(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)
    category = models.CharField(max_length=255)
    admin = models.ForeignKey(
        'users.User', related_name='stock', on_delete=models.CASCADE)

    def subtract(self, quantity: int):
        consumables = Consumable.objects.filter(
            stock=self).order_by('expiration')

        stock_items = []

        for item in consumables:
            if item.quantity != 0:
                if quantity > 0:
                    ref = item.quantity - quantity
                    if ref < 0:
                        stock_items.append(
                            {'quantity': item.quantity, 'batch': item.batch})
                        item.quantity = 0
                        item.save()
                        quantity = -ref
                    else:
                        stock_items.append(
                            {'quantity': item.quantity - ref, 'batch': item.batch})
                        item.quantity = ref
                        item.save()
                        quantity = 0

        transfered = 0

        for item in stock_items:
            transfered += item['quantity']

        return stock_items
