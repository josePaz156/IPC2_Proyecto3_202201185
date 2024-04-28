from cargarxml import lst_clientes

def generar_listado():
    listado = 'Listado:\n'
    for cliente in lst_clientes:
        nit = cliente.NIT
        nombre = cliente.nombre

        listado += f"Cliente: {nit} - {nombre}\n"
    
    return listado