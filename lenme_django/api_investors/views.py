from .serializers import InvestorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Investor
from rest_framework.views import APIView


class CreateInvestorView(APIView):
    serializer_class = InvestorSerializer

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
        investors = Investor.objects.all()
        serializer = self.serialzer_class(investors, many=True)
        return Response({"data": serializer.data})
