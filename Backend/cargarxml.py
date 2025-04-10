from clas_cliente import Cliente
from clas_banco import Banco
from clas_factura import Factura
from clas_pago import Pago
import xml.etree.ElementTree as ET
import datetime
import re
import os

lst_bancos = []
lst_clientes = []
lst_clientesNuevos = []
lst_bancosNuevos = []
lst_clientesActualizados = []
lst_bancosActualizados = []
lst_facturas = []
lst_pagos = []

def cargar_configuracion(archivo_config):
    lst_bancosActualizados.clear()
    lst_bancosNuevos.clear()
    lst_clientesActualizados.clear()
    lst_clientesNuevos.clear()
    
    try:

        xmlconfiguracion = ET.XML(archivo_config)

        for cliente in xmlconfiguracion.findall('clientes/cliente'):
            nit = cliente.find('NIT').text.strip()
            nombre_cliente = cliente.find('nombre').text.strip()

            cliente_existente = False

            # Verificar si el cliente ya existe en la lista
            for elemento in lst_clientes:
                if elemento.NIT == nit and elemento.nombre != nombre_cliente:
                    posicion = lst_clientes.index(elemento)
                    act_cliente = Cliente(nit, nombre_cliente)
                    lst_clientes[posicion] = act_cliente
                    lst_clientesActualizados.append(act_cliente)
                    cliente_existente = True
                    break

                if elemento.NIT == nit and elemento.nombre == nombre_cliente:
                    cliente_existente = True
                    break

            # Si el cliente no existe, agregarlo a la lista
            if not cliente_existente:
                new_cliente = Cliente(nit, nombre_cliente)
                lst_clientes.append(new_cliente)
                lst_clientesNuevos.append(new_cliente)

        for banco in xmlconfiguracion.findall('bancos/banco'):
            codigo = banco.find('codigo').text.strip()
            nombre_banco = banco.find('nombre').text.strip()

            banco_existente = False

            for elemento in lst_bancos:
                if elemento.codigo == codigo and elemento.nombre != nombre_banco:
                    posicion = lst_bancos.index(elemento)
                    act_banco = Banco(codigo, nombre_banco)
                    lst_bancos[posicion] = act_banco
                    lst_bancosActualizados.append(act_banco)
                    banco_existente = True
                    break

                if elemento.codigo == codigo and elemento.nombre == nombre_banco:
                    banco_existente = True
                    break
            
            if not banco_existente:
                new_banco = Banco(codigo, nombre_banco)
                lst_bancos.append(new_banco)
                lst_bancosNuevos.append(new_banco)
        
        now = datetime.datetime.now()
        nombre_archivo = "respuestaConfig_" + now.strftime("%Y%m%d_%H%M%S") + ".xml"


        configXML = respuestaConfig(nombre_archivo)

    except ET.ParseError:
        print("Error: El archivo XML no está bien formateado o contiene errores.")

    except Exception as e:
        print("Error:", e)

    lst_clientes.sort(key=lambda x: x.NIT)
    lst_bancos.sort(key=lambda x: x.codigo)

    return configXML


def respuestaConfig(nombre_archivo):

    root = ET.Element('respuesta')

    clientes = ET.SubElement(root, 'clientes')

    for cliente in lst_clientesNuevos:
        creado = ET.SubElement(clientes, "creados")
        creado.text = cliente.NIT +' - ' + cliente.nombre

    for cliente in lst_clientesActualizados:
        actualizados = ET.SubElement(clientes, 'Actualizados')
        actualizados.text = cliente.NIT +' - ' + cliente.nombre
    
    bancos = ET.SubElement(root, 'bancos')

    for banco in lst_bancosNuevos:
        creado = ET.SubElement(bancos, 'creados')
        creado.text = banco.codigo + ' - ' + banco.nombre
    
    for banco in lst_bancosActualizados:
        actualizados = ET.SubElement(bancos, 'Actualizados')
        actualizados.text = banco.codigo + ' - ' + banco.nombre

    xmlstr = ET.tostring(root, encoding='utf8', method='xml')
    formatted_xml = xmlstr.decode()
    formatted_xml = formatted_xml.replace("><", ">\n<")

    directorio_padre = os.path.dirname(os.path.abspath(__file__))
    
    # Navega un nivel hacia arriba para acceder a la carpeta "archivos"
    ruta_archivos = os.path.join(directorio_padre, "..", "Archivos/Respuestas")

    ruta_completa = os.path.join(ruta_archivos, nombre_archivo)
    
    with open(ruta_completa, "w") as file:
        file.write('<?xml version="1.0"?>\n')
        file.write(formatted_xml)

    for cliente in lst_clientes:
        print(cliente.NIT)
        print(cliente.nombre)
    
    return formatted_xml


def carga_transac(archivo_transac):

    facturas_duplicadas = 0
    factura_error = 0
    facturas_nuevas = 0
    pago_duplicado = 0
    pago_nuevo = 0
    pago_error = 0


    try:
        xmltransaccion = ET.XML(archivo_transac)

        for factura in xmltransaccion.findall('facturas/factura'):
            numero = factura.find('numeroFactura').text.strip()
            nit = factura.find('NITcliente').text.strip()
            fecha_factura_texto = factura.find('fecha').text.strip()
            valor = factura.find('valor').text.strip()

            fecha_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', fecha_factura_texto)
            if fecha_match:
                fecha_factura = fecha_match.group(1)
            else:
                fecha_factura = None

            factura_existente = False

            cliente_existente = any(cliente.NIT == nit for cliente in lst_clientes)
            if cliente_existente:

                for elemento in lst_facturas:
                    if elemento.numero == numero:
                        facturas_duplicadas += 1
                        factura_existente = True
                        break
                    
                if not factura_existente:
                    new_factura = Factura(numero, nit, fecha_factura, valor)
                    lst_facturas.append(new_factura)
                    facturas_nuevas += 1
            
            else:
                factura_error += 1

        
        for pago in xmltransaccion.findall('pagos/pago'):
            codigo = pago.find('codigoBanco').text.strip()
            fecha_pago_texto = pago.find('fecha').text.strip()
            nit_pago = pago.find('NITcliente').text.strip()
            valor_pago = pago.find('valor').text.strip()

            fecha_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', fecha_pago_texto)
            if fecha_match:
                fecha_pago = fecha_match.group(1)
            else:
                fecha_pago = None

            pago_existente = False

            banco_existente = any(banco.codigo == codigo for banco in lst_bancos)
            cliente_existente = any(cliente.NIT == nit_pago for cliente in lst_clientes)

            if banco_existente and cliente_existente:
                for elemento in lst_pagos:
                    if elemento.codigo == codigo and elemento.fecha == fecha_pago and elemento.nit == nit_pago:
                        pago_duplicado += 1
                        pago_existente = True
                        break

                if not pago_existente:
                    new_pago = Pago(codigo, fecha_pago, nit_pago, valor_pago)
                    lst_pagos.append(new_pago)
                    pago_nuevo += 1
            else:
                pago_error += 1

        now = datetime.datetime.now()
        nombre_archivo = "respuestaTransac_" + now.strftime("%Y%m%d_%H%M%S") + ".xml"

        transacXML = respuestaTransac(nombre_archivo, facturas_nuevas, facturas_duplicadas, pago_duplicado, pago_nuevo, factura_error, pago_error)    
        
    except ET.ParseError:
        print("Error: El archivo XML no está bien formateado o contiene errores.")

    except Exception as e:
        print("Error:", e)

    return transacXML

def respuestaTransac(nombre_archivo, facturas_nuevas, facturas_duplicadas, pago_duplicado, pago_nuevo, factura_error, pago_error):

    root = ET.Element('transacciones')

    facturas = ET.SubElement(root, 'facturas')


    nueva = ET.SubElement(facturas, 'nuevasFacturas')
    nueva.text = str(facturas_nuevas)

    duplicada = ET.SubElement(facturas, 'facturasDuplicadas')
    duplicada.text = str(facturas_duplicadas)

    error_fac = ET.SubElement(facturas, 'facturasConError')
    error_fac.text = str(factura_error)
    
    pagos = ET.SubElement(root, 'pagos')

    nuevo = ET.SubElement(pagos, 'nuevosPagos')
    nuevo.text = str(pago_nuevo) 

    duplicado = ET.SubElement(pagos, 'duplicadosPagos')
    duplicado.text = str(pago_duplicado)

    error_pa = ET.SubElement(pagos, 'pagosConError')
    error_pa.text = str(pago_error)

    xmlstr = ET.tostring(root, encoding='utf8', method='xml')
    formatted_xml = xmlstr.decode()
    formatted_xml = formatted_xml.replace("><", ">\n<")

    directorio_padre = os.path.dirname(os.path.abspath(__file__))
    
    ruta_archivos = os.path.join(directorio_padre, "..", "Archivos/Respuestas")

    ruta_completa = os.path.join(ruta_archivos, nombre_archivo)
    
    with open(ruta_completa, "w") as file:
        file.write('<?xml version="1.0"?>\n')
        file.write(formatted_xml)

    return formatted_xml

def inicializar():
    for cliente in lst_clientes:
        print(cliente.NIT + " - " + cliente.nombre)
    
    for banco in lst_bancos:
        print(banco.codigo+ " - " + banco.nombre)

    for factura in lst_facturas:
        print(factura.numero)

    for pago in lst_pagos:
        print(pago.codigo+ " - " + pago.nit)

    lst_clientes.clear()
    lst_bancos.clear()
    lst_facturas.clear()
    lst_pagos.clear()
    
    print(lst_bancos)
    print(lst_clientes)
    print(lst_facturas)
    print(lst_pagos)
