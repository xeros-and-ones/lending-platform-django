from .serializers import InvestorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Investor
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


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
