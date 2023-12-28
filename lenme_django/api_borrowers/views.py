from django.http import request
from rest_framework.views import APIView

from .serializers import BorrowerSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Borrower
from api_loans.models import Loan, Offer, PendingOffers
from api_loans.serializers import PendingOfferSerializer
from api_investors.models import Investor


class CreateBorrowerView(APIView):
    serializer_class = BorrowerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            borrower = serializer.save()
            return Response(
                {
                    "Message": f"{borrower.name}, you have been successfully registered as a Borrower."
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewBorrowersView(APIView):
    serializer_class = BorrowerSerializer

    def get(self, request):
        borrowers = Borrower.objects.all()
        serializer = self.serializer_class(borrowers, many=True)
        return Response({"Borrowers": serializer.data})


def interest_calculator(principle):
    interest = principle * 0.075
    total = interest + principle
    return total


class AcceptOfferView(APIView):
    serializer_class = PendingOfferSerializer

    def get_queryset(self):
        borrower_id = self.request.data.get("borrower_id")
        return Offer.objects.filter(borrower_id=borrower_id, status="PENDING")

    def post(self, request):
        print(request.data)
        req = request.data.get("offers")
        print(req)
        offer = Offer.objects.get(id=req)
        delete_pending_offer = PendingOffers.objects.get(offers=offer)
        delete_pending_offer.delete()
        delete_pending_offer.save()
        rm_offer_from_pending = PendingOffers.objects.get(offers_id=req)
        rm_offer_from_pending.delete()
        offer.status = "Accepted"
        offer.save()
        loan = Loan.objects.filter(status="PENDING").get(borrower_id=offer.borrower)
        loan.investor = offer.investor
        loan.interest_rate = offer.interest_rate
        loan.status = "Funded"
        loan.save()
        investor_balance = Investor.objects.get(id=offer.investor.id)
        investor_balance.balance -= loan.amount + 3.75
        investor_balance.save()
        final_amount_per_month = interest_calculator(loan.amount)
        return Response(
            {
                "Message": f"success {loan.amount} , {loan.period}. You will be paying ${final_amount_per_month/ loan.period} every month for {loan.period} Month(s)."
            }
        )
