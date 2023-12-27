from rest_framework import serializers
from .models import Loan, Offer


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "borrower",
            "investor",
            "amount",
            "period",
            "interest_rate",
            "status",
            "paid_amount",
        ]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ["borrower", "investor", "loan", "interest_rate", "status"]
