from django.db import models
from django.contrib.auth.models import User
from case.models import Case
# Create your models here.


class Report(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='report_case')
    lab_attendant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_lab_attendant')
    generated_date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.case
