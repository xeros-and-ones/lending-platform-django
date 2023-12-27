from rest_framework import serializers
from .models import Borrower


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ["id", "name"]
