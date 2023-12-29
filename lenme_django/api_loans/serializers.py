from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Loan, Offer, PendingOffers


class LoanSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        model = Loan
        fields = [
            "borrower",
            "amount",
            "period",
        ]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ["loan", "borrower", "investor", "interest_rate", "status"]
        read_only_fields = ["borrower", "interest_rate", "status"]


class PendingOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingOffers
        fields = ["offers"]
