from django.urls import path
from .views import MonthlyPaymentView, SimulateMonthlyPaymentsView

urlpatterns = [
    path("", MonthlyPaymentView.as_view()),
    path("sim", SimulateMonthlyPaymentsView.as_view()),
]
