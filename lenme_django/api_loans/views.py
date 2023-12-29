from rest_framework import status
from api_borrowers.models import Borrower
from api_investors.models import Investor
from rest_framework.response import Response
from .models import Loan, Offer, PendingOffers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import LoanSerializer, OfferSerializer


class LoanRequestView(APIView):
    serializer_class = LoanSerializer

    @swagger_auto_schema(
        operation_description="Submit a loan request",
        request_body=LoanSerializer,
        responses={201: "Loan request submitted successfully", 400: "Invalid input"},
    )
    def post(self, request, *args, **kwargs):
        borrower = Borrower.objects.get(id=request.data["borrower"])
        serializer = self.serializer_class(
            data={
                "borrower": borrower.id,
                "amount": request.data["amount"],
                "period": request.data["period"],
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message": "Your loan request has been successfully made.",
                    "loan": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferRequestView(APIView):
    serializer_class = OfferSerializer

    @swagger_auto_schema(
        operation_description="Submit an Offer to the borrower",
        request_body=OfferSerializer,
        responses={200: "Offer submitted successfully", 400: "Invalid input"},
    )
    def post(self, request, *args, **kwargs):
        loan = Loan.objects.get(id=request.data["loan"])
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
                pending_offer = PendingOffers.objects.create(offers=offer)
                pending_offer.save()
                offer_data = self.serializer_class(offer)
                return Response(
                    {
                        "Message": "Your offer to the borrower has been successfully submitted.",
                        "offer": offer_data.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "Message": "unfortunately the loan will not be funded due to insufficient balance."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"Message": "Your Fund seems to be very low"},
                status=status.HTTP_403_FORBIDDEN,
            )
