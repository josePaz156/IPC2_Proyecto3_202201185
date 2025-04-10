from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from xml.etree import ElementTree as ET
from cargarxml import cargar_configuracion, carga_transac, inicializar
from consulta_cuenta import generar_informe
from listado_clientes import generar_listado
from grafico import ordenar_datos

app = Flask(__name__)
CORS(app)

# AQUÍ VAN LAS RUTAS
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

@app.route('/postCargarConfig', methods=['POST'])
def cargar_xml_config():
    entradaXML = request.data
    configXML = entradaXML.decode('utf-8')
    respuesta = cargar_configuracion(configXML)
    return respuesta

@app.route('/postCargarTransac', methods=['POST'])
def cargar_xml_transac():
    entradaXML = request.data
    transacXML = entradaXML.decode('utf-8')
    respuestaTransac = carga_transac(transacXML)
    return respuestaTransac

@app.route('/postInicializar', methods=['DELETE'])
def post_inicializar():
    inicializar()
    return jsonify({"message": "Inicializacion Exitosa"})

@app.route('/getConsultarCuenta/<string:NIT>', methods=['GET'])
def consulta(NIT):
    informe = generar_informe(NIT)
    return jsonify(informe)

@app.route('/getListadoClientes', methods=['GET'])
def listado():
    listado = generar_listado()
    return listado

@app.route('/graphs', methods=['GET'])
def grafica():
    mes = request.args.get('mes')
    año = int(request.args.get('año'))

    if mes is None or año is None:
        return "Error: Debes proporcionar valores para 'mes' y 'año'", 400

    try:
        año = int(año)
    except ValueError:
        return "Error: El valor de 'año' debe ser un número entero", 400

    data = ordenar_datos(mes, año)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)