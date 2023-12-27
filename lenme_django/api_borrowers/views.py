from .serializers import BorrowerSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Borrower
from api_loans.models import Loan, Offer


@api_view(["POST"])
def create_borrower(request):
    if request.method == "POST":
        serializer = BorrowerSerializer(data=request.data)
        if serializer.is_valid():
            borrower = serializer.save()
            return Response(
                {
                    "Message": f"{borrower.name}, you have been successfully registered as a Borrower."
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Message": "Sorry not the expected HTTP Method."})


@api_view(["GET"])
def view_borrowers(request):
    if request.method == "GET":
        borrowers = Borrower.objects.all()
        serializer = BorrowerSerializer(borrowers, many=True)
        return Response({"data": serializer.data})


def accept_offer(request):
    if request.method == "POST":
        data = request.POST
        req = Offer.objects.get(borrower_id=data["borrower"])
        req.status = "Accepted"
        req.save()
        total_loan_amount = req.loan.amount + 3.75
        if req.investor.balance >= total_loan_amount:
            loan = Loan.objects.get(borrower_id=1)
            loan.investor = req.investor
            loan.interest_rate = req.interest_rate
            loan.status = "Funded"
            loan.save()
            principal_amount = loan.amount
            interest_amount = (principal_amount * loan.interest_rate) / (
                12 / loan.period
            )
            final_amount_per_month = (principal_amount + interest_amount) / loan.period
            return Response(
                {
                    "Message": f"The proposed offer has been accepted and the loan will be funded successfully. You will be paying ${final_amount_per_month} every month for {loan.period} Month(s)."
                }
            )
        else:
            return Response(
                {
                    "Message": "The proposed offer has been accepted, but unfortunately the loan will not be funded due to the investor insufficient balance."
                }
            )
    else:
        return Response({"Message": "Sorry not the expected HTTP Method."})
