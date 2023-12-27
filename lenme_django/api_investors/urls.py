from django.urls import path
from . import views

urlpatterns = [
    path("investor/create", views.create_investor),
    path("investor/view", views.view_investors),
]
