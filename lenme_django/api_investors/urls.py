from django.urls import path
from . import views

urlpatterns = [
    path("investor/create", views.CreateInvestorView.as_view()),
    path("investor/view", views.ViewInvestorsView.as_view()),
    path("investor/can-fund", views.MockInvestorCanFund.as_view()),
]
