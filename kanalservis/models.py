from django.db import models

class MyModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)


