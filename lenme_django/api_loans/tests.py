from django.core.exceptions import ObjectDoesNotExist
from django.http import response
from django.test import TestCase, Client
from api_borrowers.models import Borrower
from api_loans.models import Loan, Offer, PendingOffers
from api_investors.models import Investor
from rest_framework import status


class LoanRequestViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.borrower = Borrower.objects.create(name="John Doe")

    def test_loan_request_successful(self):
        response = self.client.post(
            "/api/borrower/loan",
            {"borrower": self.borrower.id, "amount": 5000, "period": 6},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)

    def test_loan_request_invalid_input(self):
        response = self.client.post(
            "/api/borrower/loan",
            {"borrower": self.borrower.id, "amount": -20000, "period": 12},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_loan_request_non_existent_borrower(self):
        with self.assertRaises(ObjectDoesNotExist):
            response = self.client.post(
                "/api/borrower/loan", {"borrower": 99999, "amount": 20000, "period": 12}
            )


class OfferRequestTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.borrower = Borrower.objects.create(name="John Borrow")
        self.investor = Investor.objects.create(name="John Invest", balance=10000)
        self.loan = Loan.objects.create(borrower=self.borrower, amount=5000, period=6)

    def test_offer_request_successful(self):
        response = self.client.post(
            "/api/investor/offer", {"loan": self.loan.id, "investor": self.investor.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_offer_insufficient_balance(self):
        self.investor.balance = 4000
        self.investor.save()
        response = self.client.post(
            "/api/investor/offer", {"loan": self.loan.id, "investor": self.investor.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_zero_balance(self):
        self.investor.balance = 0
        self.investor.save()
        response = self.client.post(
            "/api/investor/offer", {"loan": self.loan.id, "investor": self.investor.id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_non_existent_loan(self):
        with self.assertRaises(ObjectDoesNotExist):
            response = self.client.post(
                "/api/investor/offer", {"loan": 1000, "investor": self.investor.id}
            )


class LoanFundingProcessTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.borrower = Borrower.objects.create(name="John Borrow")
        cls.investor = Investor.objects.create(name="John Invest", balance=10000)

    def test_borrower_accept_offer(self):
        loan_response = self.client.post(
            "/api/borrower/loan",
            {"borrower": self.borrower.id, "amount": 5000, "period": 6},
        )
        loan_data = loan_response.data
        offer_response = self.client.post(
            "/api/investor/offer",
            {"loan": loan_data["loan"]["borrower"], "investor": self.investor.id},
        )
        offer_data = offer_response.data
        response = self.client.post(
            "/api/borrower/accept-offer", {"offers": offer_data["offer"]["loan"]}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Offer.objects.get(id=offer_data["offer"]["loan"]).status, "Accepted"
        )
        self.assertEqual(Loan.objects.get(borrower=self.borrower).status, "Funded")
        self.assertEqual(Investor.objects.get(id=self.investor.id).balance, 4996.25)
