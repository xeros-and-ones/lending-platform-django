from .serializers import InvestorSerializer, MockInvestorFundSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Investor
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from api_loans.models import Loan


class CreateInvestorView(APIView):
    serializer_class = InvestorSerializer

    @swagger_auto_schema(
        operation_description="Create an Investor",
        request_body=InvestorSerializer,
        responses={
            200: "Investor Created submitted successfully",
            400: "Invalid input",
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            investor = serializer.save()
            return Response(
                {
                    "Message": f"{investor.name}, you have been successfully registered as an Investor with a sufficient balance of ${investor.balance}."
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewInvestorsView(APIView):
    serialzer_class = InvestorSerializer

    def get(self, request):
        """
        View A List Of Investors
        """
        investors = Investor.objects.all()
        serializer = self.serialzer_class(investors, many=True)
        return Response({"data": serializer.data})


class MockInvestorCanFund(APIView):
    serializer_class = MockInvestorFundSerializer

    @swagger_auto_schema(
        operation_description="Simulate a borrower accepting an offer",
        request_body=MockInvestorFundSerializer,
        responses={200: "Offer accepted successfully", 400: "Invalid input"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            offer = serializer.validated_data
            loan = Loan.objects.get(id=request.data["loan"])
            investor = Investor.objects.get(id=request.data["investor"])
            if investor.balance != 0.0:
                if investor.balance >= (loan.amount + 3.75):
                    loan.status = offer["mock_borrower_accept"]
                    if loan.status == "ACCEPTED":
                        loan.status = "Funded"
                        loan.investor = investor
                        return Response(
                            {
                                "Message": "Mock Borrower Has Accepted and This Loan CAN Be Funded With these Criteria",
                                "Loan Status": loan.status,
                                "loan Investor": investor.name,
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"Message": "Invalid Criteria"},
                            status=status.HTTP_200_OK,
                        )

                else:
                    return Response(
                        {
                            "Message": "Unfortunately the loan will not be funded due to insufficient balance."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"Message": "Your Fund seems to be very low"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
