from Account.models import *
from django.db import connection

def obtener_detalles_cotizacion(id_cotizacion):
    with connection.cursor() as cursor:
        cursor.callproc('ObtenerDetallesCotizacion', [id_cotizacion])
        resultados = cursor.fetchall()
    return resultados