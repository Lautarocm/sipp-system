import requests
from django.conf import settings


class FactusolAPIError(Exception):
    """Error al comunicarse con la API de Factusol."""
    pass


class FactusolAPI:

    def __init__(self):
        self.base_url = settings.FACTUSOL_API_URL

    def _get(self, endpoint):
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, timeout=15)

            response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            raise FactusolAPIError(f"Error al consultar Factusol: {e}") from e
        except ValueError as e:
            raise FactusolAPIError("La API devolvió una respuesta JSON inválida.") from e

    def get_clients(self):
        return self._get("/api/clients")

    def get_client(self, id):
        return self._get(f"/api/clients/{id}")

    def get_products(self):
        return self._get("/api/products")

    def get_product(self, id):
        return self._get(f"/api/products/{id}")

    def get_families(self):
        return self._get("/api/families")

    def get_family(self, id):
        return self._get(f"/api/families/{id}")

    def get_orders(self, status=[]):
        return self._get(f"/api/orders{'?status='+",".join([s.trim() for s in status]) if status else ''}")

    def get_order(self, series, number):
        return self._get(f"/api/orders/{series}/{number}")

    def get_pending_products(self):
        return self._get("/api/orders/pending")

    def get_delivery_notes(self):
        return self._get("/api/delivery_notes")

    def get_delivery_note(self, series, number):
        return self._get(f"/api/delivery_notes/{series}/{number}")