from datetime import datetime

from typing import List, Dict

def construir_dict_calendario_timeline(datos:List[Dict], equivalencias:dict) -> List[Dict]:
    copia_datos = datos.copy()

    for informacion in copia_datos:
        for key_actual, _ in equivalencias.items():
            informacion[equivalencias[key_actual]] = informacion[key_actual]
            del informacion[key_actual]

        if not 'color' in informacion:
            informacion['color'] = "#B37CE1"


    copia_datos = list(map(cambiar_formato_fechas, copia_datos))
    return copia_datos


def cambiar_formato_fechas(item:dict) -> dict:
    item['start'] = item['start'].strftime("%Y-%m-%dT%H:%M:%S")
    item['end'] = item['end'].strftime("%Y-%m-%dT%H:%M:%S")

    return item