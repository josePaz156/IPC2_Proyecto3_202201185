from cargarxml import lst_clientes, lst_facturas, lst_pagos
from datetime import datetime
import json

def generar_informe(nit):
    saldo = 0
    nombre = None
    fecha = None
    lst_transacciones = []

    # Buscar el nombre del cliente
    for cliente in lst_clientes:
        print("NIT del cliente:", cliente.NIT)
        print("NIT buscado:", nit)
        if cliente.NIT == nit:
            nombre = cliente.nombre
            break

    if nombre is None:
        error = "El cliente no fue encontrado"
        return json.dumps({"error": error})  # Convertir el error a JSON y devolverlo

    # Procesar las facturas del cliente
    for factura in lst_facturas:
        if factura.NITcliente == nit:
            saldo -= int(factura.valor)
            lst_transacciones.append({
                "tipo": "factura",
                "numero": factura.numero,
                "fecha": factura.fecha,
                "valor": factura.valor
            })

    # Procesar los pagos del cliente
    for pago in lst_pagos:
        if pago.nit == nit:
            saldo += int(pago.valor)
            lst_transacciones.append({
                "tipo": "pago",
                "codigoBanco": pago.codigo,
                "fecha": pago.fecha,
                "valor": pago.valor
            })

    # Ordenar las transacciones por fecha
    lst_transacciones.sort(key=lambda x: datetime.strptime(x["fecha"], "%d/%m/%Y"))

    # Crear un diccionario con la información
    informe = {
        "nit_cliente": nit,
        "nombre_cliente": nombre,
        "saldo_anterior": saldo,
        "transacciones": lst_transacciones
    }

    # Convertir el diccionario a JSON y devolverlo

    print(informe)
    return json.dumps(informe)
