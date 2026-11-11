from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import get_orders, get_order, get_clients

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'orders/index.html')

@login_required
def orders_list(request):

    clients = get_clients()['clients']
    result = get_orders(request)

    return render(
        request,
        "orders/index.html",
        {
            "search_ref": result['search_ref'],
            "search_client_id": int(result['search_client_id']) if (result['search_client_id']) else '',
            "search_status": result['search_status'],
            "orders": result['orders'],
            "clients": {c['id']: c for c in clients},
            "error": result['error']
        }
    )

@login_required
def order_detail(request, series: str, number: int):

    result = get_order(series, number)

    return render(
        request,
        "orders/detail.html",
        {
            "order": result['order'],
            "error": result['error']
        }
    )