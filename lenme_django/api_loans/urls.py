from django.urls import path
from . import views

urlpatterns = [
    path("borrower/loan", views.LoanRequestView.as_view()),
    path("investor/offer", views.OfferRequestView.as_view()),
]
