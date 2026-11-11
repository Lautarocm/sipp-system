from services.factusol_api import (FactusolAPI, FactusolAPIError)
from datetime import datetime

def get_orders(request):

    orders = []
    error = None

    search_ref = request.GET.get("ref", "").strip()
    search_client_id = request.GET.get("client_id", "").strip()
    search_status = request.GET.get("status", "").strip()

    api = FactusolAPI()

    try:

        orders = api.get_orders(search_ref or None, search_client_id or None, search_status or None)
        
        client_ids = {o['client_id'] for o in orders}
        clients = {c['id']: c for c in api.get_clients() if c['id'] in client_ids}

        for o in orders:

            o['date'] = datetime.fromisoformat(o['date'])
            o['client'] = clients[o['client_id']]
            o['client']['name'] = o['client']['name'].split(" - ")[1] if " - " in o['client']['name'] else o['client']['name']
            del o['client_id']

    except FactusolAPIError as e:
        error = str(e)

    return {
        "search_ref": search_ref,
        "search_client_id": search_client_id,
        "search_status": search_status,
        "orders": orders,
        "error": error
    }

def get_order(series: str, number: int):

    order = None
    error = None

    api = FactusolAPI()

    try:
        order = api.get_order(series, number)
        
        order['client'] = api.get_client(order['client_id'])
        del order['client_id']

        order_products = {p['id']:p for p in api.get_products() if p['id'] in [l['product_id'] for l in order['lines']]}

        for l in order['lines']:
            l['product'] = order_products[l['product_id']]
            del l['product_id']

    except FactusolAPIError as e:
        error = str(e)

    return {
        "order": order,
        "error": error
    }

def get_clients():

    clients = []
    error = None

    api = FactusolAPI()

    try:
        clients = api.get_clients()

    except FactusolAPIError as e:
        error = str(e)

    return {
        "clients": clients,
        "error": error
    }

