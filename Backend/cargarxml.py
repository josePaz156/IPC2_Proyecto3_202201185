from clas_cliente import Cliente
from clas_banco import Banco
import xml.etree.ElementTree as ET

lst_bancos = []
lst_clientes = []
lst_transacciones = []
lst_pagos = []

def cargar_configuracion(archivo_config):
    try:
        print("Contenido del archivo XML:")
        # print(archivo_config)  # Imprimir contenido del archivo

        xmlconfiguracion = ET.XML(archivo_config)

        for cliente in xmlconfiguracion.findall('clientes/cliente'):
            nit = cliente.find('NIT').text.strip()
            nombre_cliente = cliente.find('nombre').text.strip()

            cliente_existente = False

            # Verificar si el cliente ya existe en la lista
            for elemento in lst_clientes:
                if elemento.NIT == nit:
                    posicion = lst_clientes.index(elemento)
                    act_cliente = Cliente(nit, nombre_cliente)
                    lst_clientes[posicion] = act_cliente
                    cliente_existente = True
                    break

            # Si el cliente no existe, agregarlo a la lista
            if not cliente_existente:
                new_cliente = Cliente(nit, nombre_cliente)
                lst_clientes.append(new_cliente)

        for banco in xmlconfiguracion.findall('bancos/banco'):
            codigo = banco.find('codigo').text.strip()
            nombre_banco = banco.find('nombre').text.strip()

            banco_existente = False

            for elemento in lst_bancos:
                if elemento.codigo == codigo:
                    posicion = lst_bancos.index(elemento)
                    act_banco = Banco(codigo, nombre_banco)
                    lst_bancos[posicion] = act_banco
                    banco_existente = True
                    break
            
            if not cliente_existente:
                new_banco = Banco(codigo, nombre_banco)
                lst_bancos.append(new_banco)

    except ET.ParseError:
        print("Error: El archivo XML no está bien formateado o contiene errores.")

    except Exception as e:
        print("Error:", e)

    for cliente in lst_clientes:
        print(cliente.NIT + " - " + cliente.nombre)
    
    for banco in lst_bancos:
        print(banco.codigo+ " - " + banco.nombre)

    

def repuestaConfig():

    root = ET.Element('config')

    clientes = ET.SubElement(root, 'Cliente')

    for elemento in lst_clientes:
        cliente = ET.SubElement(clientes, 'cliente')
        creado = ET.SubElement(cliente, 'NIT')
        creado.text = elemento['NIT']
        nombre = ET.SubElement(cliente, 'nombre')
        nombre.text = elemento.nombre







