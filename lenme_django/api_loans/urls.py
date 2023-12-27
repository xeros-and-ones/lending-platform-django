from django.urls import path
from . import views

urlpatterns = [
    path("borrower/loan", views.loan_request),
    path("investor/offer", views.offer_request),
]
