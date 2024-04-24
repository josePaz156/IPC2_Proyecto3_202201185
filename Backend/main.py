from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from xml.etree import ElementTree as ET
from cargarxml import cargar_configuracion

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
    cargar_configuracion(configXML)
    return jsonify({"message": "Archivo cargado Exitosamente"})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)