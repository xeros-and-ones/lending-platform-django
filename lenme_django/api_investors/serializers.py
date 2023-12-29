from rest_framework import serializers
from .models import Investor
from api_loans.models import Offer


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ["name", "balance"]


class MockInvestorFundSerializer(serializers.ModelSerializer):
    MOCK_STATUS_CHOICES = [("PENDING", "Pending"), ("ACCEPTED", "Accepted")]
    mock_borrower_accept = serializers.ChoiceField(choices=MOCK_STATUS_CHOICES)

    class Meta:
        model = Offer
        fields = [
            "loan",
            "borrower",
            "investor",
            "interest_rate",
            "status",
            "mock_borrower_accept",
        ]
        read_only_fields = ["borrower", "interest_rate", "status"]
