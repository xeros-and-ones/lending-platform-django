from api_borrowers.models import Borrower
from api_investors.models import Investor
from rest_framework.response import Response
from .models import Loan, Offer
from rest_framework.decorators import api_view


@api_view(["POST"])
def loan_request(request):
    if request.method == "POST":
        data = request.POST
        if "amount" and "period" in data:
            borrower = Borrower.objects.get(id=data["borrower"])
            req = Loan(
                borrower=borrower, amount=float(data["amount"]), period=data["period"]
            )
            req.save()
            return Response(
                {"Message": "Your loan request has been successfully made."}
            )
        else:
            return Response({"Message": "Missing one of the amount or period field."})
    else:
        return Response({"Message": "Sorry not the expected HTTP Method."})


@api_view(["POST"])
def offer_request(request):
    if request.method == "POST":
        data = request.POST
        if "interest_rate" in data:
            borrower = Borrower.objects.get(id=data["borrower"])
            investor = Investor.objects.get(id=data["investor"])
            loan = Loan.objects.get(id=data["loan"])
            req = Offer(
                borrower=borrower,
                investor=investor,
                loan=loan,
                interest_rate=float(data["interest_rate"]),
            )
            req.save()
            return Response(
                {
                    "Message": "Your offer to the borrower has been successfully submitted."
                }
            )
        else:
            return Response({"Message": "Missing the interest_rate field."})
    else:
        return Response({"Message": "Sorry not the expected HTTP Method."})
