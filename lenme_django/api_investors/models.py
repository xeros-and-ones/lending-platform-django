from django.db import models


class Investor(models.Model):
    name = models.CharField(max_length=100, blank=False)
    balance = models.FloatField(blank=False, default=0.0)

    def __str__(self):
        return f"Name: {self.name} \nBalance: {self.balance}"
