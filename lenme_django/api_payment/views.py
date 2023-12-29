from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_loans.models import Loan
from .serializers import LoanPaymentSerializer, SimLoanPaymentSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class MonthlyPaymentView(APIView):
    serializer_class = LoanPaymentSerializer

    @swagger_auto_schema(
        operation_description="Submit Monthly Payment",
        request_body=LoanPaymentSerializer,
        responses={200: "Monthly Payment submitted successfully", 400: "Invalid input"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            loan = Loan.objects.get(id=data["loan_id"])
            loan.paid_amount += data["amount_to_pay"]

            principal_amount = loan.amount / loan.period
            interest_amount = principal_amount * 0.075 / loan.period
            final_amount = principal_amount + interest_amount

            if loan.paid_amount >= final_amount * loan.period:
                loan.status = "Completed"
                loan.save()
                return Response(
                    {
                        "Message": "Congratulations! All the payments are successfully paid back to the investor."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                loan.save()
                return Response(
                    {"Message": "See you next month."}, status=status.HTTP_200_OK
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimulateMonthlyPaymentsView(APIView):
    serializer_class = SimLoanPaymentSerializer

    @swagger_auto_schema(
        operation_description="Simulate Monthly Payments",
        responses={
            200: "Monthly payments simulated successfully",
            400: "Invalid input",
        },
    )
    def post(self, request, *args, **kwargs):
        loan_id = request.data.get("loan_id")
        loan = Loan.objects.get(id=loan_id)
        print(loan)

        principal_amount = loan.amount / loan.period
        interest_amount = principal_amount * 0.075
        final_amount = principal_amount + interest_amount

        payment_log = []
        for _ in range(loan.period):
            if loan.paid_amount < final_amount:
                loan.paid_amount += final_amount
                payment_log.append(
                    {"Message": "Monthly Payment Successful, See you next month."}
                )
                if loan.paid_amount == final_amount:
                    loan.status = "Completed"

                    payment_log.append(
                        {
                            "Message": f"Monthly Payment Successful, See you next month. {loan.paid_amount}"
                        }
                    )
                    break
                return Response(payment_log)
            elif loan.paid_amount == final_amount:
                return Response(
                    {"Message": "Insufficient funds to cover the payment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"Message": f"Monthly payments simulated successfully."},
            status=status.HTTP_200_OK,
        )
