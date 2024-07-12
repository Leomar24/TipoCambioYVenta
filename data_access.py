from zeep import Client
from lxml import etree
from entities import TipoCambio
from zeep.exceptions import XMLSyntaxError

class BCCR:
    url = 'https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx?WSDL'
    correo = 'leomarzeng@gmail.com'
    token = 'LGNO71MAZA'

    def __init__(self):
        self.client = Client(self.url)

    def obtener_tasa_cambio(self, fecha, indicador):
        try:
            resultado = self.client.service.ObtenerIndicadoresEconomicosXML(
                Indicador=indicador,
                FechaInicio=fecha,
                FechaFinal=fecha,
                Nombre='Leomar',
                SubNiveles='N',
                CorreoElectronico=self.correo,
                Token=self.token
            )
            tipo_cambio = self.parsear_tipo_cambio(resultado)
            return tipo_cambio
        except Exception as e:
            raise RuntimeError(f"No se pudo obtener el tipo de cambio para la fecha {fecha} e indicador {indicador}: {str(e)}")

    def obtener_tipo_cambio(self, fecha):
        try:
            tipo_cambio_compra = self.obtener_tasa_cambio(fecha, '317')
            tipo_cambio_venta = self.obtener_tasa_cambio(fecha, '318')
            return TipoCambio(fecha, tipo_cambio_compra, tipo_cambio_venta)
        except Exception as e:
            raise RuntimeError(f"No se pudo obtener el tipo de cambio para la fecha {fecha}: {str(e)}")

    def parsear_tipo_cambio(self, xml):
        try:
            root = etree.fromstring(xml)
            
            num_valor_elem = root.find(".//NUM_VALOR")
            if num_valor_elem is None:
                raise RuntimeError("No se encontró el elemento NUM_VALOR en la respuesta XML.")

            num_valor = num_valor_elem.text
            return num_valor
        except XMLSyntaxError as e:
            raise RuntimeError(f"Error XMLSyntaxError al recibir la respuesta: {e}")
        except Exception as e:
            raise RuntimeError(f"No se pudo parsear el tipo de cambio: {str(e)}")
