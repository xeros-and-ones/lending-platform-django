from django.db import models
from api_borrowers.models import Borrower
from api_investors.models import Investor


class Loan(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("FUNDED", "Funded"),
        ("COMPLETED", "Completed"),
    ]

    borrower = models.ForeignKey(
        Borrower, on_delete=models.CASCADE, db_index=True, blank=True, null=True
    )
    investor = models.ForeignKey(
        Investor, on_delete=models.SET_NULL, db_index=True, blank=True, null=True
    )
    amount = models.IntegerField(null=False, default=0)
    period = models.IntegerField(null=False, default=6)
    interest_rate = models.FloatField(null=True, default=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    paid_amount = models.FloatField(default=0.0)

    def __str__(self):
        return (
            f"Borrower: {self.borrower} \n"
            f"Investor: {self.investor} \n"
            f"Loan Amount: {self.amount} \n"
            f"Interest Rate: {self.interest_rate} \n"
            f"Period: {self.period} Month(s) \n"
            f"Status: {self.status} \n"
            f"Setteled: {self.paid_amount}"
        )


class Offer(models.Model):
    STATUS_CHOICES = [("PENDING", "Pending"), ("ACCEPTED", "Accepted")]

    borrower = models.ForeignKey(
        Borrower, on_delete=models.CASCADE, db_index=True, blank=True, null=True
    )
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, db_index=True, blank=True, null=True
    )
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, db_index=True, blank=True, null=True
    )
    interest_rate = models.FloatField(null=False, default=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method
        PendingOffers.objects.create(offers=self)

    def __str__(self):
        return (
            f"Borrower: {self.borrower} \n"
            f"Investor: {self.investor} \n"
            f"Loan: {self.loan} \n"
            f"Interest Rate: {self.interest_rate} \n"
            f"Status: {self.status}"
        )


class PendingOffers(models.Model):
    offers = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Offers: {self.offers}"
