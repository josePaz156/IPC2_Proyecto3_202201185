from cargarxml import lst_bancos, lst_pagos
from datetime import datetime, timedelta

def ordenar_datos(mes, año):
    
    # Convertir el mes a su número correspondiente
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes_numero = meses.get(mes.lower())
    if mes_numero is None:
        raise ValueError("El nombre del mes es inválido.")

    # Obtener la fecha de inicio y fin del rango de meses
    fecha_inicio = datetime(year=año, month=mes_numero, day=1)
    fecha_fin = fecha_inicio + timedelta(days=31)  # Suponemos un mes de máximo 31 días

    # Filtrar los pagos dentro del rango de fechas
    pagos_filtrados = []
    for pago in lst_pagos:
        fecha_pago = datetime.strptime(pago.fecha, "%d/%m/%Y")
        if fecha_inicio <= fecha_pago <= fecha_fin:
            pagos_filtrados.append(pago)

    ganancias_por_banco = {}

    for pago in pagos_filtrados:
        print("Código:", pago.codigo, "Fecha:", pago.fecha, "NIT:", pago.nit, "Valor:", pago.valor)
        codigo_banco = pago.codigo
        for banco in lst_bancos:
            if codigo_banco == banco.codigo:
                nombre_banco = banco.nombre
                break
        valor_pago = float(pago.valor)
        if nombre_banco in ganancias_por_banco:
            ganancias_por_banco[nombre_banco] += valor_pago
        else:
            ganancias_por_banco[nombre_banco] = valor_pago

    print(ganancias_por_banco)

    return ganancias_por_banco

    


