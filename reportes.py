# generando reporte
from utils import fetch_data, procesar_reporte


def generar_reporte(id_reporte, start_date, end_date):
    start_date = start_date.isoformat()
    end_date = end_date.isoformat()
    payload = None

    if id_reporte == "ID_reporte_1":
        payload = {
            "startDay": start_date,
            "endDay": end_date,
            "data": [
                {"metric": "timeInCycle"},
                {"metric": "allTime"}
            ],
            "groupBy": [
                {"group": "machineGroup"},
                {"group": "machine"},
                {"group": "shift"},
                {"group": "day"}
            ],
            "exclude": {
            },
            "flatten": True
        }

    elif id_reporte == "ID_reporte_2":
        payload = {
        }

    if payload:
        data = fetch_data(payload)
        if data:
            return procesar_reporte(id_reporte, data)

    return None
