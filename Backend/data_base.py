import xml.etree.ElementTree as ET
from cargarxml import lst_clientes, lst_bancos

def escribir_data_base():

    root = ET.Element('DataBase')

    clientes = ET.SubElement(root, 'clientes')

    for cliente in lst_clientes:
        nit = ET.SubElement(clientes, 'NIT')
        nit.text = cliente.NIT