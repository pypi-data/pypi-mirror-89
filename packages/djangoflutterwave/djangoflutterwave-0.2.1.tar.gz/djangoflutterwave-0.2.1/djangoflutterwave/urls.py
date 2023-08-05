# stdlib  imports

# django imports
from django.urls import path, include

# 3rd party imports

# project imports
from djangoflutterwave.views import TransactionCreateView, TransactionDetailView


app_name = "djangoflutterwave"

urlpatterns = [
    path("transaction/", TransactionCreateView.as_view(), name="transaction_create"),
    path("<str:tx_ref>/", TransactionDetailView.as_view(), name="transaction_detail"),
]
