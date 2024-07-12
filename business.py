from data_access import BCCR
from entities import TipoCambio

class BusinessLogic:
    def __init__(self):
        self.bccr = BCCR()

    def consultar_tipo_cambio(self, fecha):
        try:
            tipo_cambio = self.bccr.obtener_tipo_cambio(fecha)
            tipo_cambio.tipo_cambio_compra = round(float(tipo_cambio.tipo_cambio_compra), 2)
            tipo_cambio.tipo_cambio_venta = round(float(tipo_cambio.tipo_cambio_venta), 2)
            return tipo_cambio
        except Exception as e:
            raise RuntimeError(f"Error al obtener los valores: {e}")
