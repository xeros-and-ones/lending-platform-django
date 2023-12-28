from rest_framework import serializers
from .models import Loan, Offer, PendingOffers


class LoanSerializer(serializers.ModelSerializer):
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
