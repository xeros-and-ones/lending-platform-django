from django.db import models


class Borrower(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"Name: {self.name} \n"
