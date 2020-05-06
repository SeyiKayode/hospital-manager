from django.db import models
from django.contrib.auth.models import User
from case.models import Case
from stock.models import Items
# Create your models here.


class Bill(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='bill_case')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='bill_item')
    amount = models.IntegerField()
    quantity = models.IntegerField()
    bill_date = models.DateField()
    bill_details = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.case.patient.username
