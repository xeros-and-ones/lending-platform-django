from rest_framework import serializers


class LoanPaymentSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()
    amount_to_pay = serializers.FloatField()


class SimLoanPaymentSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()
