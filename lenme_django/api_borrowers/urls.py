from django.urls import path
from . import views

urlpatterns = [
    path("borrower/create", views.CreateBorrowerView.as_view()),
    path("borrower/view", views.ViewBorrowersView.as_view()),
    path("borrower/accept-offer", views.AcceptOfferView.as_view()),
]
