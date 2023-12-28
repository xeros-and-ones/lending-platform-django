from django.urls import path
from .views import MonthlyPaymentView

urlpatterns = [path("", MonthlyPaymentView.as_view())]
