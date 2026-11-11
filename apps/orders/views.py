from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from services.factusol_api import (FactusolAPI, FactusolAPIError)

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'orders/index.html')

@login_required
def list_orders(request):

    orders = []
    error = None

    api = FactusolAPI()

    try:
        orders = api.get_orders()
    except FactusolAPIError as e:
        error = str(e)

    return render(
        request,
        "orders/index.html",
        {
            "orders": orders,
            "error": error
        }
    )