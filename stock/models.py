from django.db import models
import uuid
# from consumables.models import Consumable


# class CustomObj(models.Manager):
#     def subtract(self, quantity: int):
#         consumables = Consumable.objects.filter(
#             stock=self).order_by('expiration')

#         stock_items = []

#         for item in consumables:
#             if quantity > 0:
#                 ref = item.quantity - quantity
#                 if ref < 0:
#                     stock_items.append(
#                         {'quantity': f'{item.quantity} {item.unit}', 'batch': item.batch})
#                     item.quantity = 0
#                     item.save()
#                     quantity = -ref
#                 else:
#                     stock_items.append(
#                         {'quantity': f'{item.quantity - ref} {item.unit}', 'batch': item.batch})
#                     item.quantity = ref
#                     item.save()
#                     quantity = 0

#         return stock_items


class Stock(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)
    category = models.CharField(max_length=255)
    admin = models.ForeignKey(
        'users.User', related_name='stock', on_delete=models.CASCADE)

    # objects = CustomObj()
