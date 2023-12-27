from django.urls import path
from . import views

urlpatterns = [
    path("borrower/create", views.create_borrower),
    path("borrower/view", views.view_borrowers),
    path("borrower/accept-offer", views.accept_offer),
]
