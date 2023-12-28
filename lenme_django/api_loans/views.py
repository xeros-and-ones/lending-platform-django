from api_borrowers.models import Borrower
from api_investors.models import Investor
from rest_framework.response import Response
from .models import Loan, Offer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import LoanSerializer, OfferSerializer


class LoanRequestView(APIView):
    serializer_class = LoanSerializer

    def post(self, request):
        borrower = Borrower.objects.get(id=request.data["borrower"])
        serializer = self.serializer_class(
            data={
                "borrower": borrower.id,
                "amount": request.data["amount"],
                "period": request.data["period"],
            }
        )
        if serializer.is_valid():
            loan = serializer.save()
            return Response(
                {"Message": "Your loan request has been successfully made."}
            )
        else:
            return Response(serializer.errors, status=400)


class OfferRequestView(APIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        return Loan.objects.filter(status="PENDING")

    def post(self, request, *args, **kwargs):
        loan = self.get_queryset().get(id=request.data["loan"])
        print(loan.status)
        investor = Investor.objects.get(id=request.data["investor"])
        if investor.balance != 0.0:
            if investor.balance >= (loan.amount + 3.75):
                offer = Offer(
                    borrower=loan.borrower,
                    investor=investor,
                    loan=loan,
                    interest_rate=loan.interest_rate,
                )
                offer.save()
                return Response(
                    {
                        "Message": "Your offer to the borrower has been successfully submitted."
                    },
                    status=200,
                )
            else:
                return Response(
                    {
                        "Message": "unfortunately the loan will not be funded due to insufficient balance."
                    },
                    status=400,
                )
        else:
            return Response({"Message": "Your Fund seems to be very low"})
