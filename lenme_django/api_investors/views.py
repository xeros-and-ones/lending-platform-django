from .serializers import InvestorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Investor


@api_view(["POST"])
def create_investor(request):
    if request.method == "POST":
        serializer = InvestorSerializer(data=request.data)
        if serializer.is_valid():
            investor = serializer.save()
            return Response(
                {
                    "Message": f"{investor.name}, you have been successfully registered as an Investor with a sufficient balance of ${investor.balance}."
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Message": "Sorry not the expected HTTP Method."})


@api_view(["GET"])
def view_investors(request):
    if request.method == "GET":
        investors = Investor.objects.all()
        serializer = InvestorSerializer(investors, many=True)
        return Response({"data": serializer.data})
